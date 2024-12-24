from argparse import Namespace
import logging
import os
import re
from typing import Any, AsyncGenerator, Dict, List, Optional, Union
import uuid

from transformers import AutoTokenizer

from furiosa_llm.api import LLM
from furiosa_llm.outputs import CompletionOutput, RequestOutput
from furiosa_llm.sampling_params import SamplingParams
from furiosa_llm.server.parse import parse_and_batch_prompt  # type: ignore
from furiosa_llm.tokenizer import encode_auto
from furiosa_llm.utils import get_logger_with_tz

logger = get_logger_with_tz(logging.getLogger(__name__))


def load_llm_from_args(args: Namespace) -> LLM:
    model: str = args.model
    dp = args.data_parallel_size
    devices = args.devices

    speculative_model = args.speculative_model
    draft_dp = args.speculative_draft_data_parallel_size
    num_speculative_tokens = args.num_speculative_tokens

    # if model is a directory and "ready" file exists, it is an artifact
    use_artifact_from_path = os.path.isdir(model) and os.path.exists(os.path.join(model, "ready"))
    use_artifact_load_path = os.path.isdir(model) and os.path.exists(
        os.path.join(model, "artifact.json")
    )

    if (num_speculative_tokens or speculative_model) and not (
        num_speculative_tokens and speculative_model
    ):
        raise ValueError(
            "To use speculative decoding, both --num-speculative-tokens and --speculative-model should be given."
        )

    # Create LLM for speculative model if given.
    if speculative_model:
        assert num_speculative_tokens

        # FIXME(ssh): Remove this constraint after adjusting the LLM to provide a model parallelization interface for the original and speculative model seperately.
        if draft_dp != dp:
            raise ValueError(
                "Different value for --data-parallel-size and --speculative-draft-pipeline-parallel-size is not allowed now."
            )

        use_speculative_model_artifacts_from_path = os.path.isdir(
            speculative_model
        ) and os.path.exists(os.path.join(speculative_model, "ready"))
        if use_speculative_model_artifacts_from_path:
            logger.info(f"Loading Speculative model LLM from artifact: {speculative_model}")
            if any(
                [
                    args.speculative_draft_tensor_parallel_size,
                    args.speculative_draft_pipeline_parallel_size,
                ]
            ):
                logger.warning(
                    "When loading Speculative model LLM from artifact, given -tp and -pp values will be ignored."
                )
            speculative_model = LLM.from_artifacts(
                speculative_model,
                data_parallel_size=draft_dp,
                devices=devices,
            )
        else:
            draft_tp = args.speculative_draft_tensor_parallel_size or 4
            draft_pp = args.speculative_draft_pipeline_parallel_size or 1

            speculative_model = LLM(
                speculative_model,
                pipeline_parallel_size=draft_pp,
                tensor_parallel_size=draft_tp,
                data_parallel_size=draft_dp,
                devices=devices,
            )

    if use_artifact_load_path:
        logger.info(f"Loading LLM from artifact: {model}")

        return LLM.load_artifacts(
            model,
            devices=devices,
            data_parallel_size=dp,
        )

    if use_artifact_from_path:
        logger.info(f"Loading LLM from artifact: {model}")
        if any([args.tensor_parallel_size, args.pipeline_parallel_size]):
            logger.warning(
                "When loading LLM from artifact, given -tp and -pp values will be ignored."
            )
        return LLM.from_artifacts(
            model,
            speculative_model=speculative_model,
            num_speculative_tokens=num_speculative_tokens,
            data_parallel_size=dp,
            devices=devices,
        )

    if model == "furiosa-ai/fake-llm":
        return FakeLLM()

    if not is_hf_model_id_like(model):
        logger.warning(
            f"The given --model argument is not a valid artifact path, nor a valid Hugging Face model id: {model}"
        )
        logger.warning("Trying Hugging Face model id anyways.")

    tp = args.tensor_parallel_size or 4
    pp = args.pipeline_parallel_size or 1
    logger.info(
        f"Loading LLM from Hugging Face model id: {model}, pp={pp}, tp={tp}, dp={dp}, devices={devices}"
    )
    return LLM(
        model,
        speculative_model=speculative_model,
        num_speculative_tokens=num_speculative_tokens,
        pipeline_parallel_size=pp,
        tensor_parallel_size=tp,
        data_parallel_size=dp,
        devices=devices,
    )


def is_hf_model_id_like(model_id: str) -> bool:
    pattern = r"^[\w-]+/[\w.-]+$"
    return bool(re.match(pattern, model_id))


class FakeLLM(LLM):
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
        self.text_output = "Lorem ipsum dolor sit amet, consectetur adipiscing elit."
        self.token_output = self.tokenizer.encode(self.text_output)
        self.is_generative_model = True

    @property
    def model_max_seq_len(self) -> int:
        return 2048

    def generate(
        self,
        prompts: Union[str | List[str]],
        sampling_params: SamplingParams = SamplingParams(),
        prompt_token_ids: Optional[Union[List[int], List[List[int]]]] = None,
        tokenizer_kwargs: Optional[Dict[str, Any]] = None,
    ) -> RequestOutput | List[RequestOutput]:
        parsed_prompts = parse_and_batch_prompt(prompts or prompt_token_ids)
        num_prompts = len(parsed_prompts)
        prompt_strs = []
        for prompt in parsed_prompts:
            if prompt['is_tokens']:
                prompt_strs.append(
                    self.tokenizer.decode(prompt['content'], skip_special_tokens=True)
                )
            else:
                prompt_strs.append(prompt['content'])

        if num_prompts == 1:
            return self.lorem_ipsum_output(prompt_strs[0], sampling_params)
        else:
            return [self.lorem_ipsum_output(prompt, sampling_params) for prompt in prompt_strs]

    async def stream_generate(
        self,
        prompt: str,
        sampling_params: SamplingParams = SamplingParams(),
        prompt_token_ids: Optional[List[int]] = None,
        tokenizer_kwargs: Optional[Dict[str, Any]] = None,
        is_demo: bool = False,
    ) -> AsyncGenerator[str, None]:
        assert prompt_token_ids is None
        for token in self.token_output[: sampling_params.max_tokens]:
            yield self.tokenizer.decode([token], skip_special_tokens=True)

    def lorem_ipsum_output(
        self, prompt: str, sampling_params: SamplingParams, finish_reason: Optional[str] = "stop"
    ) -> RequestOutput:
        token_output = self.token_output[: sampling_params.max_tokens]
        return RequestOutput(
            # request_id will be overwritten by handlers
            request_id=uuid.uuid4().hex,
            prompt=prompt,
            prompt_token_ids=encode_auto(self.tokenizer, prompt)['input_ids'],
            outputs=[
                CompletionOutput(
                    index=0,
                    text=self.tokenizer.decode(token_output, skip_special_tokens=True),
                    token_ids=token_output,
                    finish_reason=finish_reason,
                )
            ],
            finished=True,
        )
