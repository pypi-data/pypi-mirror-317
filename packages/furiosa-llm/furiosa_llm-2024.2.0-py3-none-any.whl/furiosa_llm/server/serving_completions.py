import time
from typing import AsyncGenerator, List, Union

from fastapi import Request

from furiosa_llm.api import LLM, RequestOutput
from furiosa_llm.server.parse import (  # type: ignore
    is_list_of,
    is_token_or_tokens,
    parse_and_batch_prompt,
)
from furiosa_llm.server.protocol import (
    CompletionRequest,
    CompletionResponse,
    CompletionResponseChoice,
    CompletionResponseStreamChoice,
    CompletionStreamResponse,
    ErrorResponse,
    UsageInfo,
)
from furiosa_llm.server.serving_base import OpenAIServing
from furiosa_llm.server.utils import AnyTokenizer, merge_async_iterators, random_uuid


class OpenAIServingCompletion(OpenAIServing):
    def __init__(
        self,
        llm: LLM,
        max_model_len: int,
    ):
        # Currently we only support one model per server
        self.llm = llm
        self.model_name = llm.model_metadata.pretrained_id
        self.max_model_len = max_model_len

    async def create_completion(
        self,
        request: CompletionRequest,
        raw_request: Request,
    ) -> Union[AsyncGenerator[str, None], CompletionResponse, ErrorResponse]:
        """Completion API similar to OpenAI's API.

        See https://platform.openai.com/docs/api-reference/completions/create
        for the API specification. This API mimics the OpenAI Completion API.

        NOTE: Currently we do not support the following feature:
            - suffix (the language models we currently support do not support
            suffix)
        """
        request_id = f"cmpl-{random_uuid()}"
        created_time = int(time.time())
        prompt = request.prompt

        try:
            sampling_params = request.to_sampling_params()
        except ValueError as e:
            return self.create_error_response(str(e))

        stream = (
            request.stream
            and (request.best_of is None or request.n == request.best_of)
            and not request.use_beam_search
        )

        if stream:
            return self.completion_stream_generator(
                request,
                request_id,
                created_time,
                tokenizer=self.llm.tokenizer,
            )

        try:
            # The request accepts a sentence (or sentences), or list of token ids (or lists of token ids) as input.
            # Meanwhile, it may seem like `LLM.generate()` accepts the same types according to the type hint:
            # str | List[str] (as the `prompt` argument), and List[int] | List[List[int]] (as the `prompt_token_ids` argument).
            # However, the latter is not true; the accepted type for the `prompt_token_ids` is BatchEncoding.
            # It's a bug in type hinting.
            # To work around this, we convert token ids into str if prompt `is_token_or_tokens`.
            if is_token_or_tokens(prompt):
                if is_list_of(prompt, int):
                    prompt = self.llm.tokenizer.decode(prompt, skip_special_tokens=True)
                else:
                    prompt = [
                        self.llm.tokenizer.decode(tk_ids, skip_special_tokens=True)
                        for tk_ids in prompt
                    ]

            output = self.llm.generate(prompt, sampling_params, tokenizer_kwargs={"add_special_tokens": True})  # type: ignore
            if not isinstance(output, list):
                output = [output]
            response = self.request_output_to_completion_response(
                output, request, request_id, created_time
            )
            return response
        except ValueError as e:
            return self.create_error_response(str(e))

    async def completion_stream_generator(
        self,
        request: CompletionRequest,
        request_id: str,
        created_time: int,
        tokenizer: AnyTokenizer,
    ) -> AsyncGenerator[str, None]:
        try:
            # XXX: furiosa_llm.stream_generate accepts a single str as the prompt input and streams str as output.
            # The implementation below is designed to conform to this function's type signature,
            # resulting in unnecessary redundant encode/decode operations.
            parsed_prompts = parse_and_batch_prompt(request.prompt)
            prompt_strs: List[str] = []
            for prompt in parsed_prompts:
                if prompt['is_tokens']:
                    prompt_strs.append(tokenizer.decode(prompt['content']))
                else:
                    prompt_strs.append(prompt['content'])

            result_generator: List[AsyncGenerator[str, None]] = [
                self.llm.stream_generate(prompt, request.to_sampling_params(), tokenizer_kwargs={"add_special_tokens": True})  # type: ignore
                for prompt in prompt_strs
            ]
            merged_generator = merge_async_iterators(*result_generator)

            async for prompt_idx, res in merged_generator:
                assert request.max_tokens is not None
                # TODO: support echo

                chunk = CompletionStreamResponse(
                    id=request_id,
                    created=created_time,
                    model=self.model_name,
                    choices=[
                        CompletionResponseStreamChoice(
                            index=prompt_idx,  # TODO: support n > 1 case
                            text=res,
                            logprobs=None,  # TODO: support logprobs
                            finish_reason=None,  # TODO: support finish_reason
                            stop_reason=None,  # TODO: support stop_reason
                        )
                    ],
                )

                response_json = chunk.model_dump_json(exclude_unset=False)
                yield f"data: {response_json}\n\n"

            # TODO: support request.stream_options.include_usage

        except ValueError as e:
            data = self.create_streaming_error_response(str(e))
            yield f"data: {data}\n\n"
        yield "data: [DONE]\n\n"

    def request_output_to_completion_response(
        self,
        request_outputs: List[RequestOutput],
        _request: CompletionRequest,
        request_id: str,
        created_time: int,
    ) -> CompletionResponse:
        choices: List[CompletionResponseChoice] = []
        num_prompt_tokens = 0
        num_generated_tokens = 0

        for request_output in request_outputs:
            prompt_token_ids = request_output.prompt_token_ids

            for output in request_output.outputs:
                # TODO: support echo
                output_text = output.text
                choice_data = CompletionResponseChoice(
                    index=len(choices),
                    text=output_text,
                    finish_reason=output.finish_reason,
                )
                choices.append(choice_data)

            num_prompt_tokens += len(prompt_token_ids)
            num_generated_tokens += sum(len(output.token_ids) for output in request_output.outputs)

        usage = UsageInfo(
            prompt_tokens=num_prompt_tokens,
            completion_tokens=num_generated_tokens,
            total_tokens=num_prompt_tokens + num_generated_tokens,
        )

        return CompletionResponse(
            id=request_id,
            created=created_time,
            model=self.model_name,
            choices=choices,
            usage=usage,
        )
