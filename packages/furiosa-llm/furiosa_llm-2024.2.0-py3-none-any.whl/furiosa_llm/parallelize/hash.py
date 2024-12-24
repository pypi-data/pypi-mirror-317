import dataclasses
import hashlib
import json
import logging
import os
from time import time
from typing import Any, Mapping, Optional, Sequence, Set, Tuple, Type

import furiosa_llm_models  # type: ignore
import model_compressor_impl  # type: ignore
import torch
from torch._ops import OpOverload
from torch.fx import GraphModule, Node
from torch.fx.passes.shape_prop import TensorMetadata, _extract_tensor_metadata
from torch.utils._pytree import tree_flatten, tree_map_only
import transformers
from transformers import PretrainedConfig

from furiosa_llm.models.metadata import QuantizationConfig
from furiosa_llm.parallelize.utils import get_normalized_torch_op_node_args

logger = logging.getLogger(__file__)


def get_env_independent_hash(val: Any) -> str:
    hasher = hashlib.sha256()
    if isinstance(val, (list, tuple)):
        for elem in val:
            hasher.update(get_env_independent_hash(elem).encode())
    else:
        if dataclasses.is_dataclass(val):
            assert not isinstance(
                val, type
            )  # is_dataclass narrows down to "DataclassInstance | type[DataclassInstance]"; we expect "DataclassInstance" only
            val = json.dumps(dataclasses.asdict(val), sort_keys=True, indent=2)
        hasher.update(str(val).encode())
    return hasher.hexdigest()


def hash_model(
    original_model_type: Type,
    model_config: PretrainedConfig,
    quantization_config: Optional[QuantizationConfig],
    qformat_qparam_path: Optional[Tuple[os.PathLike, os.PathLike]],
    pretrained_id: str,
    seed: Optional[int],
    is_random_weight_model: bool,
    extra_args: Mapping[str, str] = {},
) -> str:
    if is_random_weight_model and seed is None:
        raise ValueError(
            "When `is_random_weight_model` is True, `seed` should not be None to determine weight value is same."
        )

    weight_hash = str(seed) if is_random_weight_model else pretrained_id

    to_be_hashed = [
        str(original_model_type),
        model_config.to_json_string(),
        weight_hash,
    ]

    # Add version info of the model
    if original_model_type.__module__.startswith("furiosa_llm_models"):
        to_be_hashed.append(furiosa_llm_models.__version__)
    elif original_model_type.__module__.startswith("transformers"):
        to_be_hashed.append(transformers.__version__)
    else:
        raise NotImplementedError(f"unhashable model class module: {original_model_type}")

    # Add quantization info if quantized
    if qformat_qparam_path is not None:
        mcp_version = model_compressor_impl.__version__  # e.g., '0.3.1 (rev: eb19f39d)'

        # Hash qformat, qparam files.
        start = time()
        qfile_hashes = (
            hashlib.md5(open(filename, 'rb').read()).hexdigest() for filename in qformat_qparam_path
        )
        logger.info(f"Quantization artifacts hashing takes {time() - start:.2f} seconds.")

        to_be_hashed.append(mcp_version)
        to_be_hashed.extend(qfile_hashes)
        to_be_hashed.append(str(quantization_config))

    if extra_args:
        to_be_hashed.append(json.dumps(extra_args, sort_keys=True))

    return get_env_independent_hash(to_be_hashed)


def hash_example_inputs(
    example_args: Sequence,
    example_kwargs: Mapping,
) -> str:
    return get_env_independent_hash(
        json.dumps(
            tree_map_only(
                torch.Tensor,
                lambda t: (t.shape, str(t.dtype), t.stride(), str(t.device)),
                (example_args, example_kwargs),
            ),
            sort_keys=True,
            indent=2,
        ),
    )


def _get_only_needed_tensor_meta_for_hashing(node: Node, gm: GraphModule) -> Tuple:
    example_val = node.meta.get("val")
    tensor_meta = node.meta.get("tensor_meta")
    if example_val is not None:
        tensor_meta = _extract_tensor_metadata(example_val)
    elif tensor_meta is not None:
        pass
    elif node.op == "get_attr":
        assert isinstance(node.target, str)
        example_val = getattr(gm, node.target)
        tensor_meta = _extract_tensor_metadata(example_val)
    else:
        raise ValueError(
            "There's no way to get tensor meta from node. Fill 'val' or 'tensor_meta'."
        )

    # We don't care about other information such as memory_format, requires_grad, and quantization metadata.
    return tree_map_only(TensorMetadata, lambda x: (x.shape, x.dtype, x.stride), tensor_meta)


# Are 10 iterations sufficient?
_WL_ITERATION = 10


def hash_fx_graph(gm: GraphModule) -> str:
    import networkx as nx  # type: ignore[import-untyped]

    g = nx.DiGraph()
    placeholder_cnt = 0

    type_emulation_in_out: Set
    try:
        type_emulation_in_out = {
            torch.ops.furiosa.type_emulation_in.default,
            torch.ops.furiosa.type_emulation_out.default,
        }
    except AttributeError:
        type_emulation_in_out = set()

    INFO_ATTR = "label"
    SPECIAL_MARKER_FOR_NODE = "special_marker_for_node_@#$$!##"

    for node in gm.graph.nodes:
        edges = []
        attrs = {"op": node.op}
        if node.op == "placeholder":
            attrs["idx"] = placeholder_cnt
            attrs["tensor_meta"] = _get_only_needed_tensor_meta_for_hashing(node, gm)
            placeholder_cnt += 1
        elif node.op == "get_attr":
            attrs["tensor_meta"] = _get_only_needed_tensor_meta_for_hashing(node, gm)
        elif node.op == "call_function":
            attrs["target"] = str(node.target)

            node_args = tuple(node.args)
            node_kwargs = dict(node.kwargs)

            if isinstance(node.target, OpOverload):
                node_args, node_kwargs = get_normalized_torch_op_node_args(node)

            # We don't consider Node in kwargs now. It's very rare case.
            flattened_kwargs, _ = tree_flatten(node_kwargs)
            assert all(not isinstance(x, Node) for x in flattened_kwargs)

            # type_emulation_in/out op's third argument is node's name, we don't want it to be used for hashing.
            if node.target in type_emulation_in_out:
                node_args = node_args[:2] + node_args[3:]

            node_replaced_args = tree_map_only(Node, lambda x: SPECIAL_MARKER_FOR_NODE, node_args)
            node_replaced_kwargs = tree_map_only(
                Node, lambda x: SPECIAL_MARKER_FOR_NODE, node_kwargs
            )

            attrs["args"] = node_replaced_args
            attrs["kwargs"] = node_replaced_kwargs

            # We don't consider Node in kwargs now. It's very rare case.
            flattened_kwargs, _ = tree_flatten(node_replaced_kwargs)
            assert all(not isinstance(x, Node) for x in flattened_kwargs)

            flattened_args, _ = tree_flatten(node_args)
            for i, arg in enumerate(flattened_args):
                if not isinstance(arg, Node):
                    continue
                edges.append((arg.name, node.name, {INFO_ATTR: i}))
        elif node.op == "call_module":
            # We only consider fx graph with no call_module node now (e.g., aten-level fx graph).
            raise NotImplementedError("Fx grpah containing call module node is not supported yet.")
        elif node.op == "output":
            assert len(node.kwargs) == 0
            node_replaced_args = tree_map_only(Node, lambda x: SPECIAL_MARKER_FOR_NODE, node.args)
            attrs["args"] = node_replaced_args

            flattened_args, _ = tree_flatten(node.args)
            for i, arg in enumerate(flattened_args):
                if not isinstance(arg, Node):
                    continue
                edges.append((arg.name, node.name, {INFO_ATTR: i}))
        else:
            raise NotImplementedError(node)

        class Encoder(json.JSONEncoder):
            def default(self, obj):
                if isinstance(obj, (torch.dtype, torch.device)):
                    return str(obj)
                elif isinstance(obj, (torch.memory_format, torch.layout)):
                    return ""
                else:
                    return super().default(obj)

        label = json.dumps(attrs, indent=2, sort_keys=True, cls=Encoder)
        node_attr = {INFO_ATTR: label}
        g.add_node(node.name, **node_attr)
        for src, dst, attrs in edges:
            g.add_edge(src, dst, **attrs)

    return nx.weisfeiler_lehman_graph_hash(
        g, node_attr=INFO_ATTR, edge_attr=INFO_ATTR, iterations=_WL_ITERATION
    )
