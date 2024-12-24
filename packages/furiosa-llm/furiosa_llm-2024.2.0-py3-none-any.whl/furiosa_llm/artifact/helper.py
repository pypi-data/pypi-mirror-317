import copy
import logging
import os
from pathlib import Path
from typing import List, Optional, Sequence, Set, Tuple, Type

from torch._subclasses import FakeTensorMode
import torch.distributed._tensor.ops.common_rules
from torch.utils._pytree import tree_map_only
from transformers import PretrainedConfig, PreTrainedModel

from furiosa_llm.parallelize.pipeline.builder.arg_types import InputSampleWithMeta

from ..models import ModelMetadata
from ..models.config_types import (
    Bucket,
    BucketConfig,
    KvCacheSharingAcrossBeamsConfig,
    LLMBackend,
    ManualBucketConfig,
    MinimalBucketConfig,
    PagedAttentionConfig,
)
from ..models.utils import generate_input_sample
from ..parallelize.compiler_config import CompilerConfigContext, PipelineMode
from ..parallelize.export.tensor import save_model
from ..parallelize.model_creation_info import ModelCreationInfo
from ..parallelize.mppp.api import Mppp
from ..parallelize.pipeline import Pipeline
from ..parallelize.pipeline.builder import PipelineBuilder
from ..parallelize.pipeline.types import Device, SuperTaskKind, TensorGenInfo

logger = logging.getLogger(__name__)

# TODO: do we need to relax this assumption?
_CHUNKED_PREFILL_BUCKETS_BATCH_SIZE = 1


def generate_input_samples(
    model_config: PretrainedConfig,
    buckets: Sequence[Bucket],
    kv_cache_dtype: Optional[torch.dtype],
    paged_attention_config: Optional[PagedAttentionConfig],
    kv_cache_shaing_across_beams_config: Optional[KvCacheSharingAcrossBeamsConfig],
    is_packed_optimized: bool,
    compact_causal_mask_for_bert: bool,
    use_causal_mask_for_prefill: bool,
    need_args_for_speculative_decoding: bool,
    is_quantized: bool,
    go_through_mcp: bool,
    is_sliced_model: bool,
    prefill_pipeline_mode: PipelineMode,
    decode_pipeline_mode: PipelineMode,
    original_model_type: Type,
    compiler_config_context: CompilerConfigContext,
    add_prefill_last_block_slice: bool,
) -> Sequence[InputSampleWithMeta]:

    def extract_tensor_info(tensor: torch.Tensor) -> TensorGenInfo:
        return TensorGenInfo(shape=tensor.shape, dtype=tensor.dtype)

    with FakeTensorMode(allow_non_fake_inputs=True):
        input_samples_with_name = list()
        for bucket in buckets:
            input_sample_data = generate_input_sample(
                model_config,
                bucket,
                kv_cache_dtype,
                paged_attention_config,
                kv_cache_shaing_across_beams_config,
                is_packed_optimized,
                compact_causal_mask_for_bert,
                use_causal_mask_for_prefill,
                need_args_for_speculative_decoding,
                go_through_mcp,
                is_sliced_model,
            )
            input_sample_data = tree_map_only(torch.Tensor, extract_tensor_info, input_sample_data)
            model_name = (
                f"Quantized_{original_model_type.__module__}.{original_model_type.__name__}"
                if is_quantized
                else f"{original_model_type.__module__}.{original_model_type.__name__}"
            )
            # Please reflect the implementation of PipelineName in furiosa-llm-tests/src/e2e_base.rs
            # TODO: save needed information in Pipeline's metadata, instead of saving it in pipeline name.
            pipeline_name = f"{model_name}-kv{bucket.kv_cache_size}-b{bucket.batch_size}-attn{bucket.attention_size}"
            compiler_config_context = copy.deepcopy(compiler_config_context)

            if bucket.is_prefill:
                compiler_config_context.phase = prefill_pipeline_mode
            elif bucket.is_decode:
                compiler_config_context.phase = decode_pipeline_mode
            else:
                # FIXME: change this to proper phase config
                compiler_config_context.phase = PipelineMode.UNKNOWN
            compiler_config_context.bucket = bucket

            input_samples_with_name.append(
                InputSampleWithMeta(
                    args_data=[],  # assumed LLM models have kwargs only
                    kwargs_data=input_sample_data,
                    pipeline_name=pipeline_name,
                    compile_config=compiler_config_context,
                    add_last_block_slice=add_prefill_last_block_slice and bucket.is_prefill,
                )
            )
        return input_samples_with_name


def build_pipelines(
    model: ModelCreationInfo,
    config: PretrainedConfig,
    buckets: Sequence[Bucket],
    devices: Sequence[Device],
    param_file_path: Optional[os.PathLike],
    cache_dir: Optional[Path],
    backend: LLMBackend,
    mppp: Mppp,
    comp_supertask_kind: SuperTaskKind,
    one_supertask_per_device: bool,
    use_blockwise_compile: bool,
    do_decompositions_for_model_rewrite: bool,
    kv_cache_dtype: Optional[torch.dtype],
    paged_attention_config: Optional[PagedAttentionConfig],
    sparse_select_version: str,
    kv_cache_shaing_across_beams_config: Optional[KvCacheSharingAcrossBeamsConfig],
    tmp_dir: Optional[os.PathLike],
    model_metadata: ModelMetadata,
    # current context: model_qname, beam_size
    compiler_config_context: CompilerConfigContext,
    num_pipeline_builder_workers: int,
    num_compile_workers: int,
    embed_all_constants_into_graph: bool,
    num_blocks_per_supertask: int,
    add_prefill_last_block_slice: bool,
    is_generative_model: bool,
    param_saved_format: str = "safetensors",
    **kwargs,
) -> List[Pipeline]:
    if backend.is_parallelism_supported():
        prefill_pipeline_mode = (
            PipelineMode.LLM_PREFILL if is_generative_model else PipelineMode.UNKNOWN
        )
        decode_pipeline_mode = (
            PipelineMode.LLM_DECODE if is_generative_model else PipelineMode.UNKNOWN
        )

        assert param_file_path is not None, "parameter saved file must be given when using pipeline"
        assert tmp_dir is not None

        # do pre-compile first, and generate a pipelines with fx.graph supertask
        is_beam_search_kv_cache_sharing_model = (
            model_metadata.is_beam_search_kv_cache_sharing_model()
        )

        pipeline_builder = PipelineBuilder(
            model,
            config,
            tmp_dir,
            is_beam_search_kv_cache_sharing_model=is_beam_search_kv_cache_sharing_model,
        )
        is_packed_optimized = model_metadata.optimize_options.optimize_packed
        compact_causal_mask_for_bert = model_metadata.is_compact_causal_mask_for_bert()
        use_causal_mask_for_prefill = model_metadata.optimize_options.causal_mask_free_decoding
        need_args_for_speculative_decoding = model_metadata.supports_speculative_decoding
        is_quantized = model_metadata.is_quantized

        if isinstance(model, PreTrainedModel):
            original_model_type = model.original_type
        else:
            assert isinstance(model, ModelCreationInfo)
            original_model_type = model.metadata.get_optimized_cls()

        input_samples_in_metadata_with_name = generate_input_samples(
            model_config=config,
            buckets=buckets,
            kv_cache_dtype=kv_cache_dtype,
            paged_attention_config=paged_attention_config,
            kv_cache_shaing_across_beams_config=kv_cache_shaing_across_beams_config,
            is_packed_optimized=is_packed_optimized,
            compact_causal_mask_for_bert=compact_causal_mask_for_bert,
            use_causal_mask_for_prefill=use_causal_mask_for_prefill,
            need_args_for_speculative_decoding=need_args_for_speculative_decoding,
            is_quantized=is_quantized,
            go_through_mcp=model.metadata.need_quant_artifacts,
            is_sliced_model=model.metadata.optimize_options.calculate_logit_only_for_last_token,
            prefill_pipeline_mode=prefill_pipeline_mode,
            decode_pipeline_mode=decode_pipeline_mode,
            original_model_type=original_model_type,
            compiler_config_context=compiler_config_context,
            add_prefill_last_block_slice=add_prefill_last_block_slice,
        )

        pipelines = pipeline_builder.build_pipelines(
            devices=devices,
            mppp=mppp,
            input_samples_in_metadata_with_name=input_samples_in_metadata_with_name,
            param_file_path=param_file_path,
            comp_supertask_kind=comp_supertask_kind,
            cache_dir=cache_dir,
            one_supertask_per_device=one_supertask_per_device,
            use_blockwise_compile=use_blockwise_compile,
            do_decompositions_for_model_rewrite=do_decompositions_for_model_rewrite,
            sparse_select_version=sparse_select_version,
            embed_all_constants_into_graph=embed_all_constants_into_graph,
            num_blocks_per_supertask=num_blocks_per_supertask,
            padding_block_idx=(
                paged_attention_config.padding_block_idx if paged_attention_config else None
            ),
            param_saved_format=param_saved_format,
            num_pipeline_builder_workers=num_pipeline_builder_workers,
            num_compile_workers=num_compile_workers,
        )

        return pipelines
    else:
        raise ValueError(f"unsupported backend: {backend}")


def _get_buckets_for_chunked_prefill(
    max_seq_len: int,
    chunk_size: int,
) -> List[Bucket]:
    assert chunk_size <= max_seq_len

    share, remainder = divmod(max_seq_len, chunk_size)
    buckets = []

    # XXX: We only consider buckets with batch 1 if chunked prefill is used.
    for i in range(1, share + 1):
        buckets.append(
            Bucket(
                _CHUNKED_PREFILL_BUCKETS_BATCH_SIZE,
                i * chunk_size,
                (i - 1) * chunk_size,
            )
        )
    if remainder:
        buckets.append(
            Bucket(
                _CHUNKED_PREFILL_BUCKETS_BATCH_SIZE,
                max_seq_len,
                share * chunk_size,
            )
        )
    return buckets


def get_buckets(
    bucket_config: BucketConfig,
    is_generative_model: bool,
    max_seq_len_to_capture: int,
    num_speculative_tokens: Optional[int],
    prefill_chunk_size: Optional[int],
) -> Tuple[List[Bucket], List[Bucket], List[Bucket]]:
    if isinstance(bucket_config, MinimalBucketConfig):
        assert bucket_config.max_seq_len == max_seq_len_to_capture
        # If chunked prefill is used, original prefill buckets are not used.
        if not prefill_chunk_size:
            prefill_buckets = [Bucket.prefill(1, max_seq_len_to_capture)]
        decode_buckets = [Bucket.decode(1, max_seq_len_to_capture)] if is_generative_model else []
    elif isinstance(bucket_config, ManualBucketConfig):
        if not prefill_chunk_size:
            prefill_buckets = [Bucket.prefill(*bucket) for bucket in bucket_config.prefill_buckets]
        else:
            # If chunked prefill is used, original prefill buckets are not used.
            if bucket_config.prefill_buckets:
                logger.warning(
                    "`prefill_chunk_size` is given. All given manual prefill buckets is ignored."
                )
        if is_generative_model:
            # FIXME: This is a temporary workaround to support empty decode bucket case,
            # just for getting fx graphs using `LLM.get_splitted_gms` without creating `NativeLLMEngine`.
            if bucket_config.decode_buckets is None:
                raise ValueError("decode_buckets must be given for generative models.")
            decode_buckets = [Bucket.decode(*bucket) for bucket in bucket_config.decode_buckets]
        else:
            if bucket_config.decode_buckets:
                logger.warning(
                    "decode_buckets will be ignored because the model is not a generative model."
                )
            decode_buckets = []
    else:
        raise ValueError(f"Invalid bucket config: {bucket_config}")

    other_buckets: Set[Bucket] = set()

    # Generate buckets for speculative decoding if needed.
    if num_speculative_tokens is not None:
        if num_speculative_tokens == 0:
            raise ValueError("`num_speculative_tokens` must be larger than 0.")
        other_buckets.update(
            Bucket(
                bucket.batch_size,
                bucket.attention_size,
                # NOTE: Why input_ids length become (num_speculative_tokens + 1) instead of num_speculative_tokens?
                # Whenever target model verifies draft model's sugges tokens, it generates exactly one bonus token regardless
                # of how many suggestion tokens are actually accepted. And at the time of next verification, this bonus token
                # (from previous verification) should be given as an input_ids (not kv cache!) because there is no kv cache for this bonus token.
                # So input_ids length for each verification should be num_speculative_tokens + 1 (for bonus token).
                bucket.attention_size - (num_speculative_tokens + 1),
            )
            for bucket in decode_buckets
        )

    if prefill_chunk_size:
        prefill_buckets = []
        if prefill_chunk_size > max_seq_len_to_capture:
            raise ValueError(
                "`prefill_chunk_size` should be smaller than `max_seq_len_to_capture`."
            )
        buckets_for_chunked_prefill = _get_buckets_for_chunked_prefill(
            max_seq_len_to_capture, prefill_chunk_size
        )
        for bucket in buckets_for_chunked_prefill:
            if bucket.is_prefill:
                # Expect only one prefill bucket exists.
                assert not prefill_buckets
                prefill_buckets.append(bucket)
            else:
                other_buckets.add(bucket)

    return prefill_buckets, decode_buckets, list(other_buckets)


def instantiate_and_save_model(
    model_metadata: ModelMetadata,
    use_random_weight: bool,
    qformat_path: Optional[os.PathLike],
    qparam_path: Optional[os.PathLike],
    path: os.PathLike,
    quant_ckpt_file_path: Optional[os.PathLike] = None,
) -> None:
    if use_random_weight:
        if quant_ckpt_file_path:
            raise ValueError(
                "`quant_ckpt_file_path` will be ignored when random weight model is used."
            )
        model_ = model_metadata.random_weight_model(
            qformat_path=qformat_path,
            qparam_path=qparam_path,
        )
    else:
        model_ = model_metadata.pretrained_model(
            qformat_path=qformat_path,
            qparam_path=qparam_path,
            quant_ckpt_file_path=quant_ckpt_file_path,
        )
    save_model(model_, path)
