from abc import ABC
import dataclasses
from dataclasses import dataclass
from enum import Enum
import json
import os
import re
import typing
from typing import Dict, List

import torch
from typing_extensions import TypeAlias


class ReduceOp(Enum):
    SUM = "sum"
    AVG = "avg"
    MAX = "max"
    MIN = "min"

    def __repr__(self) -> str:
        return self.value


class Placement(ABC): ...


@dataclass(frozen=True)
class Partial(Placement):
    reduce_op: ReduceOp
    type: str = "partial"

    def __post_init__(self):
        assert self.type == "partial"


@dataclass(frozen=True)
class Shard(Placement):
    dim: int
    type: str = "shard"

    def __post_init__(self):
        assert self.type == "shard"


@dataclass(frozen=True)
class Replicate(Placement):
    type: str = "replicate"

    def __post_init__(self):
        assert self.type == "replicate"


NodeId: TypeAlias = str


class DeviceMesh(List):
    def __post_init__(self):
        try:
            torch.tensor(self, dtype=torch.int)
        except Exception:
            raise ValueError(
                "DeviceMesh must be a n-dimensional int type array with fixed dimension sizes"
            )


@dataclass
class ShardSpec:
    placements: List[Placement]
    mesh: DeviceMesh

    def _to_brief_str(self) -> str:
        return f"({self.placements}, {self.mesh})"


class TensorId(NodeId): ...


NPU_PE_RANGE_IDX_RE = re.compile(r"(\d)-(\d)")
POSSIBLE_FUSION_GRANULARITY = {1, 2, 4, 8}


def _verify_device(device: str) -> None:
    kind, *rest = device.split(":")
    if kind == "cpu":
        if rest and (len(rest) != 1 or not rest[0].isdigit()):
            raise ValueError(f"Invalid device string: {device}")
    elif kind == "cuda":
        if len(rest) != 1 or not rest[0].isdigit():
            raise ValueError(f"Invalid device string: {device}")
    elif kind == "npu":
        # Example of allowed formats: "npu:0:0", "npu:1:*", npu:1:0-3"
        if len(rest) != 2:
            raise ValueError(f"Invalid device string: {device}")
        if not rest[0].isdigit():
            raise ValueError(f"Invalid npu index: {rest[0]}")

        if rest[1].isdigit():
            if int(rest[1]) > 7:
                raise ValueError(f"Invalid pe index: {rest[1]}")
        elif NPU_PE_RANGE_IDX_RE.match(rest[1]):
            start_, end_ = rest[1].split("-")
            start, end = int(start_), int(end_) + 1  # Make end inclusive
            core_range = end - start
            if core_range in POSSIBLE_FUSION_GRANULARITY and end % core_range == 0:
                pass
            else:
                raise ValueError(f"Invalid pe index range: {rest[1]}")
        elif rest[1] == "*":
            pass
        else:
            raise ValueError(f"Invalid device string: {device}")
    else:
        raise ValueError(f"Invalid device string: {device}")


# TODO: move this to furiosa-llm/device.py
class Device(str):

    def __init__(self, val: str):
        _verify_device(val)

    @property
    def kind(self) -> str:
        return self.split(":", maxsplit=1)[0]

    def to_torch_device_with_cpu_idx(self) -> torch.device:
        kind, *idx = self.split(":")

        # Npu cannot be converted to torch device. So consider it as CPU for now.
        # TODO: fix this to cover all kind of representations for NPU once it's estabilished.
        if kind in ("npu", "rngd"):
            return torch.device("cpu")
        elif len(idx) <= 1:
            idx_ = map(int, idx)
            return torch.device(kind, *idx_)
        else:
            raise ValueError(f"device {self} cannot be converted to torch device.")

    def to_torch_device(self) -> torch.device:
        # Ignore device index if kind is "cpu".
        kind, *idx = self.split(":")
        if kind == "cpu":
            return torch.device("cpu")
        else:
            return self.to_torch_device_with_cpu_idx()

    @property
    def num_pe(self) -> int:
        kind, *rest = self.split(":")
        if kind != "npu":
            raise NotImplementedError("num_pe should not be called for non-npu devices.")

        # XXX: device notation such as npu:-1 is possible for warboy,
        # but in the scope of llm it is safe to assume that the device is rngd, and len(rest) == 2.
        # but this might change in the future.
        if len(rest) != 2:
            raise ValueError(f"Invalid device string: {self}")
        pe = rest[1]

        split = pe.split("-")
        if len(split) == 1:
            return 1
        elif len(split) == 2:
            start, end = split
            return int(end) - int(start) + 1
        else:
            raise ValueError(f"Invalid device string: {self}")

    @property
    def idx(self) -> int:
        return int(self.split(":")[1])

    @property
    def pe_idx(self) -> str:
        kind, *rest = self.split(":")

        if kind != "npu":
            raise ValueError("Only npu devices have pe indexes.")

        if len(rest) != 2:
            raise ValueError(f"Invalid npu device string: {self}")

        return self.split(":")[-1]


@dataclass
class DynamicTensorSpec:
    src: NodeId
    dst: NodeId
    spec: ShardSpec

    def __iter__(self):
        yield self.src
        yield self.dst
        yield self.spec


class MpppConfigEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, torch.Tensor):
            return obj.tolist()
        elif isinstance(obj, ReduceOp):
            return obj.value
        return super().default(obj)


class SerializationError(Exception):
    def __init__(self, message):
        super().__init__(message)


def _dict_to_dataclass(cls, data):
    if isinstance(data, (str, int)):
        return cls(data)
    elif dataclasses.is_dataclass(cls):
        obj = cls(**data)  # type: ignore[assignment]
        type_hints = typing.get_type_hints(cls)
        for f in dataclasses.fields(cls):
            name = f.name
            new_field_obj = _dict_to_dataclass(type_hints[name], getattr(obj, name))
            setattr(obj, name, new_field_obj)
        return obj
    elif isinstance(data, list) and typing.get_origin(cls) is list:
        d_type = typing.get_args(cls)[0]
        return [_dict_to_dataclass(d_type, d) for d in data]
    elif isinstance(data, dict) and typing.get_origin(cls) is dict:
        k_type, v_type = typing.get_args(cls)
        return {
            _dict_to_dataclass(k_type, k): _dict_to_dataclass(v_type, v) for k, v in data.items()
        }
    else:
        try:
            if isinstance(data, dict):
                obj = cls(**data)
            else:
                obj = cls(data)
        except TypeError:
            for subclass in cls.__subclasses__():
                try:
                    obj = subclass(**data)
                    return obj
                except TypeError:
                    pass
            raise SerializationError(f"Cannot deserialize {data} to {cls}")
    return data


class DeviceId(str): ...


@dataclass
class MpppConfig:
    name: str
    devices: Dict[DeviceId, Device]
    static_tensors: Dict[TensorId, ShardSpec]
    dynamic_tensors: List[DynamicTensorSpec]

    @classmethod
    def from_str(cls, val: str) -> "MpppConfig":
        return _dict_to_dataclass(cls, json.loads(val))

    @classmethod
    def load(cls, path: os.PathLike) -> "MpppConfig":
        with open(path, "r") as f:
            return cls.from_str(f.read())

    def to_json(self) -> str:
        return json.dumps(
            dataclasses.asdict(self),
            cls=MpppConfigEncoder,
            indent=4,
            allow_nan=False,
            sort_keys=True,
        )

    def export(self, path: os.PathLike):
        with open(path, "w") as f:
            f.write(self.to_json())
