import argparse
from argparse import ArgumentParser
import asyncio
from dataclasses import dataclass, fields
import os
from pathlib import Path
from typing import AsyncGenerator, Dict, List, Literal, Optional, Tuple, Union

from transformers import BatchEncoding, PreTrainedTokenizerBase
from typing_extensions import TypedDict

from furiosa.native_runtime.llm import NativeLLMEngine, NativeRequestOutput  # type: ignore
from furiosa_llm.api import (
    CACHE_DIR,
    LLM,
    CompletionOutput,
    LLMBackend,
    RequestOutput,
    SamplingParams,
    SchedulerConfig,
    TokenizerModeType,
)


# adopted from https://github.com/vllm-project/vllm/blob/main/vllm/inputs/data.py
class TextPrompt(TypedDict):
    """Schema for a text prompt."""

    prompt: str
    """The input text to be tokenized before passing to the model."""


class TokensPrompt(TypedDict):
    """Schema for a tokenized prompt."""

    prompt_token_ids: List[int]
    """A list of token IDs to pass to the model."""


SingletonPrompt = Union[str, TextPrompt, TokensPrompt]

# TODO: support ExplicitEncoderDecoderPrompt later
PromptType = Union[SingletonPrompt]


@dataclass
class EngineArgs:
    # Currently only artifact path is supported
    model: str
    num_speculative_tokens: Optional[int] = None
    use_speculative_decoding_if_possible: bool = True
    data_parallel_size: Optional[int] = None
    tokenizer: Optional[str] = None
    tokenizer_mode: TokenizerModeType = "auto"
    seed: Optional[int] = None
    devices: Optional[str] = None
    cache_dir: os.PathLike = CACHE_DIR
    backend: Optional[LLMBackend] = None
    paged_attention_num_blocks: Optional[int] = None

    # scheduler_config
    npu_queue_limit: Optional[int] = None
    max_processing_samples: Optional[int] = None
    spare_blocks_ratio: Optional[float] = None
    is_offline: Optional[bool] = None

    speculative_model_paged_attention_num_blocks: Optional[int] = None
    packing_type: Literal["IDENTITY"] = "IDENTITY"

    @staticmethod
    def add_cli_args(parser: ArgumentParser) -> ArgumentParser:
        """Shared CLI arguments for vLLM engine."""

        # Model arguments
        parser.add_argument(
            '--model',
            type=str,
            required=True,
            help='Path to the LLM engine artifact (Pretrained id will be supported in the future releases).',
        )
        parser.add_argument(
            '--num-speculative-tokens',
            type=int,
            default=EngineArgs.num_speculative_tokens,
            help='The number of tokens that specualtive model will generate speculatively during each iteration of the decoding process.',
        )
        parser.add_argument(
            '--tokenizer',
            type=str,
            default=EngineArgs.tokenizer,
            help='The name or path of a HuggingFace Transformers tokenizer.',
        )
        parser.add_argument(
            '--tokenizer-mode',
            type=str,
            default=EngineArgs.tokenizer_mode,
            help='The tokenizer mode. "auto" will use the fast tokenizer '
            'if available, and "slow" will always use the slow tokenizer.',
        )
        parser.add_argument(
            '--seed',
            type=int,
            default=EngineArgs.seed,
            help='The seed to initialize the random number generator for sampling.',
        )

        # Furiosa LLM specific arguments
        parser.add_argument(
            '--devices',
            type=str,
            default=EngineArgs.devices,
            help='The devices to run the model. It can be a single device or a list of devices. '
            'Each device can be either "npu:X" or "npu:X:*" where X is a specific device index. '
            'If not given, available devices will be used.',
        )
        parser.add_argument(
            '--data-parallel-size',
            type=int,
            default=EngineArgs.data_parallel_size,
            help='The size of the data parallelism group. '
            'If not given, it will be inferred from total avaialble PEs and other parallelism degrees.',
        )
        parser.add_argument(
            '--cache-dir',
            type=Path,
            default=EngineArgs.cache_dir,
            help='The devices to run the model. It can be a single device or a list of devices. '
            'Each device can be either "npu:X" or "npu:X:*" where X is a specific device index. '
            'If not given, available devices will be used.',
        )
        parser.add_argument(
            '--backend',
            type=str,
            default=EngineArgs.backend,
            help='The backend implementation to run forward() of a model for the LLM. '
            'If not specified, the backend will be chosen based on the device kind.',
        )
        parser.add_argument(
            '--paged-attention-num-blocks',
            type=int,
            default=EngineArgs.paged_attention_num_blocks,
            help='The maximum number of blocks that each k/v storage per layer can store. '
            'This argument must be given if model uses paged attention.',
        )
        parser.add_argument(
            '--npu-queue-limit',
            type=int,
            default=EngineArgs.npu_queue_limit,
            help='The NPU queue limit of the scheduler config.',
        )
        parser.add_argument(
            '--max-processing-samples',
            type=int,
            default=EngineArgs.max_processing_samples,
            help='The maximum processing samples. Used as an hint for the scheduler.',
        )
        parser.add_argument(
            '--spare-blocks-ratio',
            type=float,
            default=EngineArgs.spare_blocks_ratio,
            help='The spare blocks ratio. Used as an hint for the scheduler.',
        )
        parser.add_argument(
            '--is-offline',
            type=bool,
            default=EngineArgs.is_offline,
            help='If True, the scheduler will assume the workload will be offline scenario.',
        )
        parser.add_argument(
            '--use-speculative-decoding-if-possible',
            type=bool,
            default=EngineArgs.use_speculative_decoding_if_possible,
            help="If True, speculative decoding will be used if possible "
            "(`speculative_model` is given or there's artifacts for specualtive model in the artifacts.). "
            "Otherwise, speculative decoding will not be used.",
        )
        parser.add_argument(
            '--speculative-model-paged-attention-num-blocks',
            type=int,
            default=EngineArgs.speculative_model_paged_attention_num_blocks,
            help='The maximum number of blocks that each k/v storage per layer can store for the specualtive model. '
            'This argument must be given if the specualtive model uses paged attention.',
        )
        parser.add_argument(
            '--packing-type',
            type=str,
            default=EngineArgs.packing_type,
            help='Packing algorithm. Possible values are "IDENTITY" only for now',
        )

        return parser

    @classmethod
    def from_cli_args(cls, args: argparse.Namespace):
        attrs = [attr.name for attr in fields(cls)]
        engine_args = cls(**{attr: getattr(args, attr) for attr in attrs})
        return engine_args


@dataclass
class AsyncEngineArgs(EngineArgs):
    # TODO: add async-specific arguments

    @staticmethod
    def add_cli_args(parser: ArgumentParser) -> ArgumentParser:
        # TODO: add async-specific arguments
        parser = EngineArgs.add_cli_args(parser)
        return parser


# TODO: currently LLMEngine wraps LLM, but the relationship must be inverted
class LLMEngine:
    def __init__(
        self,
        native_engine: NativeLLMEngine,
        tokenizer,
    ):
        self.native_engine = native_engine
        self.tokenizer = tokenizer

        # Queue[Tuple[request_id, NativeRequestOutput]]
        self.queue: asyncio.Queue[Tuple[str, NativeRequestOutput]] = asyncio.Queue()
        self.unfinished = 0

        # Dict[request_id, Tuple[prompt, prompt_token_ids]]
        self.prompt_cache: Dict[str, Tuple[str, List[int]]] = {}

        # vllm's accumulates output tokens between each step() calls.
        # To mimic the behavior, we store outputs and update them in each step() call.
        self.outputs: Dict[str, List[CompletionOutput]] = {}

        self.aio_loop = asyncio.new_event_loop()

    @classmethod
    def from_llm(cls, llm: LLM) -> "LLMEngine":
        return cls(llm.engine, llm.tokenizer)

    @classmethod
    def from_engine_args(cls, args: EngineArgs) -> "LLMEngine":
        try:
            scheduler_config_ = SchedulerConfig.load(f"{args.model}/scheduler_config.json")
            for scheduler_config_attr in fields(SchedulerConfig):
                if v := getattr(args, scheduler_config_attr.name, None) is not None:
                    setattr(scheduler_config_, scheduler_config_attr.name, v)
        except Exception:
            scheduler_config_ = None

        llm = LLM.from_artifacts(
            path=args.model,
            num_speculative_tokens=args.num_speculative_tokens,
            use_speculative_decoding_if_possible=args.use_speculative_decoding_if_possible,
            data_parallel_size=args.data_parallel_size,
            tokenizer=args.tokenizer,
            tokenizer_mode=args.tokenizer_mode,
            seed=args.seed,
            devices=args.devices,
            cache_dir=args.cache_dir,
            backend=args.backend,
            paged_attention_num_blocks=args.paged_attention_num_blocks,
            scheduler_config=scheduler_config_,
            speculative_model_paged_attention_num_blocks=args.speculative_model_paged_attention_num_blocks,
            packing_type=args.packing_type,
        )

        return cls.from_llm(llm)

    def add_request(
        self,
        request_id: str,
        prompt: PromptType,
        sampling_params: Optional[SamplingParams] = None,
    ) -> None:
        prompt_str, batch_encoding = preprocess_prompt(prompt, self.tokenizer)
        prompt_token_ids = batch_encoding["input_ids"]
        self.unfinished += 1
        self.prompt_cache[request_id] = (
            prompt_str,
            prompt_token_ids,
        )
        self.aio_loop.create_task(
            self._process_request(request_id, batch_encoding, sampling_params)
        )

    async def _process_request(
        self,
        request_id: str,
        batch_encoding: BatchEncoding,
        sampling_params: Optional[SamplingParams] = None,
    ) -> None:
        async for output in self.native_engine.stream_generate(batch_encoding, sampling_params):
            await self.queue.put((request_id, output))

    def has_unfinished_requests(self) -> bool:
        return self.unfinished > 0

    def step(self) -> List[RequestOutput]:
        output: NativeRequestOutput
        req_id, output = self.aio_loop.run_until_complete(self.queue.get())
        # currently only single output is supported inside `hf_compat_stream_generate`
        # if the behavior is changed, this part should be updated accordingly
        assert len(output.outputs) == 1
        prompt_str, prompt_token_ids = self.prompt_cache[req_id]

        if req_id not in self.outputs:
            completion_outputs = [
                CompletionOutput(
                    index=0,
                    text=self.tokenizer.decode(
                        o.token_ids, True, clean_up_tokenization_spaces=True
                    ),
                    token_ids=o.token_ids,
                    finish_reason=o.finish_reason,
                )
                for o in output.outputs
            ]
            self.outputs[req_id] = completion_outputs
        else:
            for i, o in enumerate(output.outputs):
                self.outputs[req_id][i].token_ids.extend(o.token_ids)
                self.outputs[req_id][i].text = self.tokenizer.decode(
                    self.outputs[req_id][i].token_ids, True, clean_up_tokenization_spaces=True
                )
                self.outputs[req_id][i].finish_reason = o.finish_reason
        completion_outputs = self.outputs[req_id]

        finished = all(o.finish_reason is not None for o in output.outputs)
        if finished:
            self.unfinished -= 1
            del self.prompt_cache[req_id]
            del self.outputs[req_id]
        return [
            RequestOutput(
                request_id=req_id,
                prompt=prompt_str,
                prompt_token_ids=prompt_token_ids,
                outputs=completion_outputs,
                finished=finished,
            )
        ]


class AsyncLLMEngine:
    def __init__(
        self,
        native_engine: NativeLLMEngine,
        tokenizer,
    ):
        self.native_engine = native_engine
        self.tokenizer = tokenizer

    @classmethod
    def from_llm(cls, llm: LLM) -> "AsyncLLMEngine":
        return cls(llm.engine, llm.tokenizer)

    @classmethod
    def from_engine_args(cls, args: AsyncEngineArgs) -> "AsyncLLMEngine":
        try:
            scheduler_config_ = SchedulerConfig.load(f"{args.model}/scheduler_config.json")
            for scheduler_config_attr in fields(SchedulerConfig):
                if v := getattr(args, scheduler_config_attr.name, None) is not None:
                    setattr(scheduler_config_, scheduler_config_attr.name, v)
        except Exception:
            scheduler_config_ = None

        llm = LLM.from_artifacts(
            path=args.model,
            num_speculative_tokens=args.num_speculative_tokens,
            use_speculative_decoding_if_possible=args.use_speculative_decoding_if_possible,
            data_parallel_size=args.data_parallel_size,
            tokenizer=args.tokenizer,
            tokenizer_mode=args.tokenizer_mode,
            seed=args.seed,
            devices=args.devices,
            cache_dir=args.cache_dir,
            backend=args.backend,
            paged_attention_num_blocks=args.paged_attention_num_blocks,
            scheduler_config=scheduler_config_,
            speculative_model_paged_attention_num_blocks=args.speculative_model_paged_attention_num_blocks,
            packing_type=args.packing_type,
        )

        return cls.from_llm(llm)

    async def generate(
        self,
        prompt: PromptType,
        sampling_params: SamplingParams,
        request_id: str,
    ) -> AsyncGenerator[RequestOutput, None]:
        async for output in self.add_request(
            request_id,
            prompt,
            sampling_params,
        ):
            yield output

    async def add_request(
        self,
        request_id: str,
        prompt: PromptType,
        sampling_params: Optional[SamplingParams] = None,
    ) -> AsyncGenerator[RequestOutput, None]:
        prompt_str, batch_encoding = preprocess_prompt(prompt, self.tokenizer)
        prompt_token_ids = batch_encoding["input_ids"]
        completion_outputs = None
        async for output in self.native_engine.stream_generate(batch_encoding, sampling_params):
            if completion_outputs is None:
                completion_outputs = [
                    CompletionOutput(
                        index=0,
                        text=self.tokenizer.decode(
                            o.token_ids, True, clean_up_tokenization_spaces=True
                        ),
                        token_ids=o.token_ids,
                        finish_reason=o.finish_reason,
                    )
                    for o in output.outputs
                ]
            else:
                for i, o in enumerate(output.outputs):
                    completion_outputs[i].token_ids.extend(o.token_ids)
                    completion_outputs[i].text = self.tokenizer.decode(
                        completion_outputs[i].token_ids, True, clean_up_tokenization_spaces=True
                    )
                    completion_outputs[i].finish_reason = o.finish_reason
            yield RequestOutput(
                request_id=request_id,
                prompt=prompt_str,
                prompt_token_ids=prompt_token_ids,
                outputs=completion_outputs,
                finished=all(o.finish_reason is not None for o in output.outputs),
            )

    # TODO
    # async def engine_step(self): ...
    # async def abort(self, request_id): ...


def preprocess_prompt(
    prompt: PromptType, tokenizer: PreTrainedTokenizerBase
) -> Tuple[str, BatchEncoding]:
    if isinstance(prompt, str):
        prompt_str = prompt
    elif isinstance(prompt, dict):
        if "prompt" in prompt:
            prompt_str = prompt["prompt"]  # type: ignore
        elif "prompt_token_ids" in prompt:
            # To get BatchEncoding, decode first and then encode again.
            # This is inefficient but since generator takes BatchEncoding as input this is the safest way.
            prompt_str = tokenizer.decode(prompt["prompt_token_ids"], skip_special_tokens=True)
        else:
            raise ValueError(f"Unsupported prompt type: {type(prompt)}")
    else:
        raise ValueError(f"Unsupported prompt type: {type(prompt)}")
    return prompt_str, tokenizer(prompt_str, padding=False, add_special_tokens=True)
