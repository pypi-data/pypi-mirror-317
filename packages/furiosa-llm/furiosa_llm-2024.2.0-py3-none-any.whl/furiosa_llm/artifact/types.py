import json
import logging
import os
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

from pydantic import BaseModel, RootModel

from ..models import ModelMetadata
from ..models.config_types import GeneratorConfig, ModelRewritingConfig, ParallelConfig

logger = logging.getLogger(__name__)


class ArtifactVersion(BaseModel):
    furiosa_llm: str
    furiosa_compiler: str


class ArtifactMetadata(BaseModel):
    artifact_id: str
    name: str
    timestamp: int
    version: ArtifactVersion


class Artifact(BaseModel):
    metadata: ArtifactMetadata

    devices: str
    generator_config: GeneratorConfig
    hf_config: Dict[str, Any]
    model_metadata: ModelMetadata
    model_rewriting_config: ModelRewritingConfig
    parallel_config: ParallelConfig

    pipelines: List[Dict[str, Any]] = []

    def append_pipeline(self, pipeline_dict: Dict[str, Any]):
        self.pipelines.append(pipeline_dict)

    def export(self, path: Union[str, os.PathLike]):
        with open(path, "w") as f:
            f.write(RootModel[Artifact](self).model_dump_json(indent=2))

    @classmethod
    def load(cls, path: Union[str, os.PathLike]) -> "Artifact":
        try:
            with open(path) as f:
                o = json.load(f)
                return Artifact(**o)
        except Exception as e:
            logger.error(e)
            raise ValueError("Artifact schema mismatched.")


class RuntimeConfig(BaseModel):
    """
    * npu_queue_limit: Maximum number of tasks that can be queued in the hardward
    * max_processing_samples: Maximum number of samples that can be processed by the scheduler
    * spare_blocks_ratio: Ratio of spare blocks that are reserved by scheduler. Smaller value will force the scheduler to use dram aggressively
    * is_offline: If True, use strategies optimzed for offline scenario
    * paged_attention_num_blocks: The maximum number of blocks that each k/v storage per layer can store.
    * prefill_chunk_size: Prefill chunk size used for chunked prefill.
    """

    npu_queue_limit: int
    max_processing_samples: int
    spare_blocks_ratio: float
    is_offline: bool
    paged_attention_num_blocks: Optional[int] = None
    prefill_buckets: Optional[Sequence[Tuple[int, int]]] = None
    decode_buckets: Optional[Sequence[Tuple[int, int]]] = None
    prefill_chunk_size: Optional[int] = None

    def export(self, path: Union[str, os.PathLike]):
        with open(path, "w") as f:
            f.write(RootModel[RuntimeConfig](self).model_dump_json(indent=2))

    @classmethod
    def load(cls, path: Union[str, os.PathLike]) -> "RuntimeConfig":
        with open(path) as f:
            o = json.load(f)
            return RuntimeConfig(**o)
