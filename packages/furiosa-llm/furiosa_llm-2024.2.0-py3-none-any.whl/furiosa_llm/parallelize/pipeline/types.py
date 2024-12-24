import copy
import dataclasses
from dataclasses import dataclass
from enum import Enum
import json
import os
from pathlib import PosixPath
import typing
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union, cast

from furiosa_torch_ext.torch_ext import preprocess
from safetensors import safe_open
import torch
from torch._subclasses import FakeTensorMode
from torch.fx import GraphModule, Node
from torch.fx.passes.shape_prop import ShapeProp

from furiosa_llm.parallelize.compiler_config import BlockType
from furiosa_llm.parallelize.export.graphmodule import deserialize_gm
from furiosa_llm.parallelize.export.tensor import ParamfileFormat, ParamFileInfo
import furiosa_llm.parallelize.model_rewriter.mppp_config as mrw
from furiosa_llm.parallelize.mppp.config import Device, DeviceId
from furiosa_llm.parallelize.node_meta import get_spec

SCHEMA_VERSION = "0.1.0"


class DataBlobId(str): ...


class ParamFileId(str): ...


class Placements(List[Tuple[int, int]]):
    @staticmethod
    def from_spec(
        spec: mrw.ShardSpec, device_id: mrw.DeviceId, unsharded_tensor_shape: Sequence[int]
    ) -> "Placements":
        device_mesh = spec.mesh
        indexes = device_mesh.get_coordinate(device_id)
        _range: List[Tuple[int, int]] = [(0, s) for s in unsharded_tensor_shape]

        cur_device_group = device_mesh.to_torch_tensor()

        assert len(indexes) == len(spec.placements)
        for index, placement in zip(indexes, spec.placements):
            # we assume there is no tensor with partial placement among input, output and weight tensors.
            assert not placement.is_partial()
            if placement.is_shard():
                shard = cast(mrw.Shard, placement)
                group_size = len(cur_device_group)
                # assume there's at most one sharding for each dimension
                assert _range[shard.dim][0] == 0
                length = _range[shard.dim][1] - _range[shard.dim][0]
                chunk_size = length // group_size

                _range[shard.dim] = (
                    chunk_size * index,
                    chunk_size * (index + 1),
                )
                # don't consider uneven sharding now.
                assert length % group_size == 0, "We only consider even partitioning"
            cur_device_group = cur_device_group[index]
        return Placements(_range)

    @staticmethod
    def from_node(node: Node) -> "Placements":
        spec = get_spec(node)
        assert isinstance(spec, mrw.ShardSpec), spec
        device_id = node.meta["device_id"]

        unsharded_shape = list(node.meta["tensor_meta"].shape)
        for placement, group_size in zip(spec.placements, spec.mesh.to_torch_tensor().shape):
            if not placement.is_shard():
                continue
            shard = cast(mrw.Shard, placement)
            unsharded_shape[shard.dim] *= group_size

        return Placements.from_spec(spec, device_id, unsharded_shape)


@dataclass
class ParamValue:
    param_file: ParamFileId
    name: str
    name_in_graph: str  # name in graph/dfg
    placements: Placements


def get_pipeline_dtype(torch_dtype: torch.dtype) -> str:
    converter = {
        "int8": "i8",
        "uint8": "u8",
        "float32": "f32",
        "float64": "f64",
        "int64": "i64",
        "int32": "i32",
        "bfloat16": "bf16",
        "bool": "bool",
    }

    original_name = str(torch_dtype)
    assert original_name.startswith("torch."), original_name
    name = original_name[6:]
    assert name in converter, f"not supported dtype: {torch_dtype}"

    return converter[name]


class Dtype(str):
    def __new__(cls, dtype: Union[str, torch.dtype]):
        if isinstance(dtype, str):
            return super().__new__(cls, dtype)
        elif isinstance(dtype, torch.dtype):
            return super().__new__(cls, get_pipeline_dtype(dtype))
        else:
            raise ValueError(f"Invalid dtype: {dtype}")

    def to_torch_dtype(self) -> torch.dtype:
        if self == "f32":
            return torch.float32
        elif self == "f64":
            return torch.float64
        elif self == "i64":
            return torch.int64
        elif self == "i32":
            return torch.int32
        elif self == "bf16":
            return torch.bfloat16
        elif self == "bool":
            return torch.bool
        elif self == "i8":
            return torch.int8
        elif self == "u8":
            return torch.uint8
        else:
            raise NotImplementedError(f"Not supported dtype: {self}")


@dataclass
class ParamInfo:
    shape: List[int]
    dtype: Dtype
    value: ParamValue


@dataclass
class TensorInfo:
    shape: List[int]
    dtype: Dtype

    @classmethod
    def from_node_tensor_meta_data(
        cls, t: torch.fx.passes.shape_prop.TensorMetadata
    ) -> "TensorInfo":
        return cls(shape=list(t.shape), dtype=Dtype(t.dtype))

    @classmethod
    def from_node(cls, node: torch.fx.Node) -> "TensorInfo":
        return cls.from_node_tensor_meta_data(node.meta["tensor_meta"])

    def __eq__(self, other):
        if not isinstance(other, TensorInfo):
            return False
        return self.shape == other.shape and self.dtype == other.dtype

    def __hash__(self):
        return hash((tuple(self.shape), self.dtype))


@dataclass
class TensorInfoWithPlacement(TensorInfo):
    placements: Placements

    @classmethod
    def from_tensor_info(
        cls, tensor_info: TensorInfo, placements: Placements
    ) -> "TensorInfoWithPlacement":
        return cls(shape=tensor_info.shape, dtype=tensor_info.dtype, placements=placements)

    @classmethod
    def from_node(cls, node: Node) -> "TensorInfoWithPlacement":
        placements = Placements.from_node(node)
        return cls.from_tensor_info(TensorInfo.from_node(node), placements)


class SuperTaskKind(str, Enum):
    # computation supertask kind
    DFG = "dfg"
    FX = "fx"
    EDF = "edf"

    # source, sink supertasks
    INPUT = "input"
    OUTPUT = "output"

    # comm ops
    SEND = "send"
    RECV = "recv"
    REDUCE = "reduce"
    ALL_REDUCE = "all_reduce"
    GATHER = "gather"
    ALL_GATHER = "all_gather"
    REDUCE_SCATTER = "reduce_scatter"
    ALLTOALL = "all_to_all"
    BROADCAST = "broadcast"

    @staticmethod
    def from_str(val: str) -> "SuperTaskKind":
        return SuperTaskKind(val)

    def to_ir_kind(self) -> str:
        ret = _SUPERTASK_KIND_TO_IR_KIND.get(self, None)
        if ret is None:
            raise ValueError(f"{self} cannot be converted to target ir")
        return ret


_SUPERTASK_KIND_TO_IR_KIND = {
    SuperTaskKind.DFG: "dfg",
    SuperTaskKind.EDF: "edf",
}


class NameAfterMakeFx(str): ...


class NameBeforeTransform(str): ...


@dataclass
class SuperTask:
    kind: SuperTaskKind
    inputs: List[NameAfterMakeFx]
    outputs: List[NameAfterMakeFx]

    def is_input(self) -> bool:
        return self.kind is SuperTaskKind.INPUT

    def is_output(self) -> bool:
        return self.kind is SuperTaskKind.OUTPUT


@dataclass
class InOutputSuperTask(SuperTask): ...


@dataclass
class SuperTaskWithDevice(SuperTask):
    device: DeviceId


@dataclass
class TensorGenInfo:
    # this is our adoption of class `TensorMetadata` from torch.fx.passes.shape_prop
    shape: torch.Size
    dtype: torch.dtype


@dataclass
class CompSuperTask(SuperTaskWithDevice):
    data: Optional[str] = None  # serialized data
    data_blob: Optional[DataBlobId] = None  # id for data blob

    def __post_init__(self):
        if self.data is None and self.data_blob is None:
            raise ValueError("Either data or data_blob should not be None")


CommMetaVal = Union[int, str]


@dataclass
class CommSuperTask(SuperTaskWithDevice):
    group: Optional[str]
    device_idx: int
    metadata: Dict[str, CommMetaVal]


@dataclass
class MetadataTensor(TensorInfo):
    idx: int

    def __eq__(self, other):
        if not isinstance(other, MetadataTensor):
            return False
        return super().__eq__(other) and self.idx == other.idx


@dataclass
class MetadataTensorSlice:
    placements: Placements
    origin: str
    dtype: Dtype
    device: DeviceId


@dataclass
class MetadataTensors:
    inputs: Dict[NameBeforeTransform, MetadataTensor]
    outputs: Dict[NameBeforeTransform, MetadataTensor]


@dataclass
class MetadataTensorSlices:
    inputs: Dict[NameAfterMakeFx, MetadataTensorSlice]
    outputs: Dict[NameAfterMakeFx, MetadataTensorSlice]


@dataclass()
class MetaData:
    tensors: MetadataTensors
    tensor_slices: MetadataTensorSlices


class SuperTaskId(str): ...


class SerializationError(Exception):
    def __init__(self, message):
        super().__init__(message)


class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, PosixPath):
            return str(obj.absolute())
        return super().default(obj)


def _dict_to_dataclass(cls, data):
    if isinstance(cls, str):
        assert isinstance(data, str)
        return cls(data)
    elif typing.get_origin(cls) == typing.Union and type(None) in typing.get_args(cls):
        if data is None:
            return None
        ty_args = typing.get_args(cls)
        assert len(ty_args) == 2
        return _dict_to_dataclass(ty_args[0], data)
    elif dataclasses.is_dataclass(cls):
        obj = cls(**data)  # type: ignore[assignment]
        type_hints = typing.get_type_hints(cls)
        for f in dataclasses.fields(cls):
            name = f.name
            new_field_obj = _dict_to_dataclass(type_hints[name], getattr(obj, name))
            setattr(obj, name, new_field_obj)
        return obj
    elif isinstance(data, list):
        origin_cls = typing.get_origin(cls)

        if origin_cls in (list, tuple):
            if len(data) == 0:
                return origin_cls(data)
            d_type = typing.get_args(cls)[0]
            return origin_cls(_dict_to_dataclass(d_type, d) for d in data)
        else:
            assert origin_cls is None
            if cls == Placements:
                data = [tuple(d) for d in data]
            return cls(data)
    elif len(typing.get_args(cls)) == 0:
        assert not isinstance(data, dict)
        return cls(data)
    elif typing.get_origin(cls) == typing.Union:
        if cls == CommMetaVal:
            # NOTE: to prevent union subtype reordering when calling typing.get_args.
            cls = CommMetaVal
        d_types = typing.get_args(cls)
        for d_type in d_types:
            try:
                return _dict_to_dataclass(d_type, data)
            except Exception:
                pass
        raise SerializationError(f"Cannot deserialize {data} to {cls}")
    elif isinstance(data, dict):
        k_type, v_type = typing.get_args(cls)
        return {
            _dict_to_dataclass(k_type, k): _dict_to_dataclass(v_type, v) for k, v in data.items()
        }
    return data


# n-dimensional array whose all leaf elements are ``DeviceId``s.
@dataclass
class TopologyDeviceConstraint(List): ...


@dataclass
class DeviceConstraint:
    kind: str
    devices: TopologyDeviceConstraint


def load_partial_param(
    param_file_path: Union[os.PathLike, str],
    tensor_name: str,
    placements: Placements,
    format: ParamfileFormat = ParamfileFormat.SAFETENSORS,
    *,
    cache: Dict[Any, Any],
    device: str = "cpu",
) -> torch.Tensor:
    if format == format.__class__.SAFETENSORS:
        try:
            f = cache[param_file_path, device]
        except KeyError:
            f = cache[param_file_path, device] = safe_open(
                param_file_path, framework="pt", device=device
            )
        # If tensor is a shared tensor and not stored, get stored one.
        if metadata := f.metadata():
            tensor_name = metadata.get(tensor_name, tensor_name)
        if not placements:
            # if tensor is scalar value with 0 dim.
            tensor = f.get_tensor(tensor_name)
            if tensor.dim() > 0:
                raise ValueError(
                    f"tensor {tensor_name} is not scalar even if its placements is empty"
                )
            return tensor
        tensor_slice = f.get_slice(tensor_name)
        return tensor_slice[[slice(*p) for p in placements]]
    else:
        raise NotImplementedError(f"param save format {format} is not supported yet")


@dataclass
class Pipeline:
    name: str
    devices: Dict[DeviceId, Device]
    tensors: Dict[NameAfterMakeFx, Union[TensorInfo, ParamInfo]]
    supertasks: Dict[SuperTaskId, Union[InOutputSuperTask, CompSuperTask, CommSuperTask]]
    metadata: MetaData
    blobs: Dict[DataBlobId, str]
    param_files: Dict[ParamFileId, ParamFileInfo]
    device_constraints: List[DeviceConstraint]
    version: str = SCHEMA_VERSION

    def to_json(self) -> str:
        return json.dumps(dataclasses.asdict(self), cls=EnumEncoder, indent=4, allow_nan=False)

    @classmethod
    def from_dict(cls, val: Dict[str, Any]) -> "Pipeline":
        return _dict_to_dataclass(cls, val)

    def export(self, path: Union[str, os.PathLike]):
        with open(path, "w+") as f:
            f.write(self.to_json())

    @classmethod
    def load(cls, path: Union[str, os.PathLike]):
        with open(path) as f:
            pipeline_dict = json.load(f)
            return cls.from_dict(pipeline_dict)

    def get_blob_kind(self) -> Dict[DataBlobId, SuperTaskKind]:
        return {
            task.data_blob: task.kind
            for _, task in self.supertasks.items()
            if isinstance(task, CompSuperTask) and task.data_blob
        }

    # FIXME: This method is highly coupled to MLPerf context.
    def get_block_type_from_supertask_id(self, task_id: SuperTaskId) -> BlockType:
        supertask = self.supertasks[task_id]
        if not isinstance(supertask, CompSuperTask):
            return BlockType.WHOLE
        if not len(self.blobs) == 3:
            return BlockType.WHOLE
        num_comp_supertasks = len(
            [task for task in self.supertasks.values() if isinstance(task, CompSuperTask)]
        )
        if len(supertask.outputs) != 1:
            return BlockType.WHOLE
        output_tensor_idx = int(supertask.outputs[0].split("_")[-1].lstrip("c"))

        if output_tensor_idx == 0:
            return BlockType.FIRST
        elif output_tensor_idx == num_comp_supertasks - 1:
            return BlockType.LAST
        else:
            return BlockType.MID

    def shallow_copy_with_replaced_devices(self, old_to_new: Dict[Device, Device]) -> "Pipeline":
        if set(old_to_new.keys()) != set(self.devices.values()):
            raise ValueError("`old_to_new` should have mappings for all original devices")

        new_devices = {dev_id: old_to_new[old_dev] for dev_id, old_dev in self.devices.items()}

        copied = copy.copy(self)
        copied.devices = new_devices
        return copied

    def eq_except_for_param_files(self, other: "Pipeline") -> bool:
        other_shallow_copy = copy.copy(other)
        other_shallow_copy.param_files = self.param_files
        return other_shallow_copy == self

    def get_gms(
        self, get_input_constants: bool = False
    ) -> Union[
        Tuple[GraphModule, ...], Tuple[Tuple[GraphModule, Tuple[Optional[torch.Tensor], ...]], ...]
    ]:
        """Get sub GraphModules in the pipeline."""

        ret: List = []
        gm_cache: Dict[Optional[DataBlobId], GraphModule] = {}

        # Sort supertasks by id to guarantee consistent order.
        sorted_supertasks = (
            supertask for _, supertask in sorted(self.supertasks.items(), key=lambda x: int(x[0]))
        )

        for supertask in sorted_supertasks:
            if not isinstance(supertask, CompSuperTask):
                continue

            if supertask.kind != SuperTaskKind.FX:
                raise ValueError("Supertask is not FX graph supertask.")

            param_load_cache: Dict[Any, Any] = {}

            fake_mode = FakeTensorMode(allow_non_fake_inputs=True)

            with fake_mode:
                fake_example_inputs = tuple(
                    torch.zeros(
                        self.tensors[input_].shape,
                        dtype=self.tensors[input_].dtype.to_torch_dtype(),
                    )
                    for input_ in supertask.inputs
                )

            gm = gm_cache.get(supertask.data_blob, None)
            if gm is None:
                if supertask.data is not None:
                    data = supertask.data
                else:
                    assert supertask.data_blob is not None
                    data = self.blobs[supertask.data_blob]

                gm = deserialize_gm(data)
                # NOTE: This Shape propagation is required because tensor meta infomration is lost during serialization. We need to regenerate this.
                ShapeProp(gm).propagate(*fake_example_inputs)
                # preprocess gms for it to be compiled immediately
                gm = preprocess(gm, fake_example_inputs)

                if supertask.data_blob is not None:
                    gm_cache[supertask.data_blob] = cast(GraphModule, gm)

            if get_input_constants:
                # TODO: change this to share same tensor among slices.
                def load_tensor(tensor_name) -> Optional[torch.Tensor]:
                    tensor_info = self.tensors[tensor_name]
                    if isinstance(tensor_info, TensorInfo):
                        # If it's not an input constant tensor (i.e., input tensor not originated from constant tensor),
                        # just return None.
                        return None
                    else:
                        assert isinstance(tensor_info, ParamInfo)
                        param_value = tensor_info.value
                        param_file_info = self.param_files[param_value.param_file]

                        return load_partial_param(
                            param_file_info.path,
                            param_value.name,
                            param_value.placements,
                            param_file_info.format,
                            cache=param_load_cache,
                        ).contiguous()

                example_input = tuple(load_tensor(input_name) for input_name in supertask.inputs)
                ret.append((gm, example_input))
            else:
                ret.append(gm)

        return tuple(ret)
