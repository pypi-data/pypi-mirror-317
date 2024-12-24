from logging import Logger
import time
from typing import AsyncGenerator, List, Optional, Union

from fastapi import Request
from jinja2 import Template

from furiosa_llm.api import LLM, RequestOutput, SamplingParams
from furiosa_llm.server.protocol import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatCompletionResponseStreamChoice,
    ChatCompletionStreamResponse,
    ChatMessage,
    DeltaMessage,
    ErrorResponse,
    UsageInfo,
)
from furiosa_llm.server.serving_base import OpenAIServing
from furiosa_llm.server.utils import ConversationMessage, apply_chat_template, random_uuid

logger = Logger(__name__)


class OpenAIServingChat(OpenAIServing):
    # XXX: We currently use transformers == 4.31, which does not support tokenizer-oriented chat template.
    # So we get chat_template as a required parameter in the constructor.
    def __init__(
        self,
        llm: LLM,
        model_max_seq_len: int,
        chat_template: str,
        response_role: str = "assistant",
    ):
        self.llm = llm
        self.model_name = llm.model_metadata.pretrained_id
        self.model_max_seq_len = model_max_seq_len
        self.chat_template = Template(chat_template)
        self.response_role = response_role

    async def create_chat_completion(
        self,
        request: ChatCompletionRequest,
        raw_request: Optional[Request] = None,
    ) -> Union[AsyncGenerator[str, None], ChatCompletionResponse, ErrorResponse]:
        """Completion API similar to OpenAI's API.

        See https://platform.openai.com/docs/api-reference/chat/create
        for the API specification. This API mimics the OpenAI
        ChatCompletion API.
        """
        try:
            messages = [ConversationMessage(m) for m in request.messages]  # type: ignore
            # TODO: check if request.chat_template is given, and use it
            # for request.chat_template, use lru_cache to avoid recompilation
            prompt_str: str = apply_chat_template(
                messages,
                self.chat_template,
                self.llm.tokenizer,
            )
        except Exception as e:
            logger.error("Error in applying chat template from request: %s", e)
            return self.create_error_response(str(e))

        # XXX: prompt_str already contains special tokens, so we don't need to add special tokens.
        try:
            sampling_params = request.to_sampling_params()
        except ValueError as e:
            return self.create_error_response(str(e))

        request_id = f"chat-{random_uuid()}"

        stream = (
            request.stream
            and (request.best_of is None or request.n == request.best_of)
            and not request.use_beam_search
        )
        if stream:
            return self.chat_completion_stream_generator(
                request, request_id, prompt_str, sampling_params
            )

        try:
            output = self.llm.generate(prompts=prompt_str, sampling_params=sampling_params)
        except ValueError as e:
            # TODO(vllm): Use a vllm-specific Validation Error
            return self.create_error_response(str(e))

        try:
            return self.chat_completion_response(
                output,  # type: ignore
                request_id,
            )
        except ValueError as e:
            # TODO(vllm): Use a vllm-specific Validation Error
            return self.create_error_response(str(e))

    def get_chat_request_role(self, request: ChatCompletionRequest) -> str:
        if request.add_generation_prompt:
            return self.response_role
        else:
            return request.messages[-1]["role"]

    async def chat_completion_stream_generator(
        self,
        request: ChatCompletionRequest,
        request_id: str,
        prompt_str: str,
        sampling_params: SamplingParams,
    ) -> AsyncGenerator[str, None]:
        model_name = self.model_name
        created_time = int(time.time())
        chunk_object_type = "chat.completion.chunk"
        first_iteration = True

        # TODO: support n > 1

        try:
            async for res in self.llm.stream_generate(prompt_str, sampling_params):
                # We need to do it here, because if there are exceptions in
                # the result_generator, it needs to be sent as the FIRST
                # response (by the try...catch).
                if first_iteration:
                    # Send first response for each request.n (index) with
                    # the role
                    role = self.get_chat_request_role(request)
                    choice_data = ChatCompletionResponseStreamChoice(
                        index=0, delta=DeltaMessage(role=role), logprobs=None, finish_reason=None
                    )
                    chunk = ChatCompletionStreamResponse(
                        id=request_id,
                        object=chunk_object_type,  # type: ignore
                        created=created_time,
                        choices=[choice_data],
                        model=model_name,
                    )
                    data = chunk.model_dump_json(exclude_unset=True)
                    yield f"data: {data}\n\n"

                    # TODO: support request.stream_options.include_usage
                    # TODO: support request.echo

                    first_iteration = False

                # TODO: support logprobs
                # TODO: support handling of finish_reason and stop_reason
                delta_text = res
                delta_message = DeltaMessage(content=delta_text)
                choice_data = ChatCompletionResponseStreamChoice(
                    index=0, delta=delta_message, logprobs=None, finish_reason=None
                )
                chunk = ChatCompletionStreamResponse(
                    id=request_id,
                    object=chunk_object_type,  # type: ignore
                    created=created_time,
                    choices=[choice_data],
                    model=model_name,
                )
                data = chunk.model_dump_json(exclude_unset=True)
                yield f"data: {data}\n\n"
            # TODO: support request.stream_options.include_usage

        except ValueError as e:
            # TODO(vllm): Use a vllm-specific Validation Error
            data = self.create_streaming_error_response(str(e))
            yield f"data: {data}\n\n"
        # Send the final done message after all response.n are finished
        yield "data: [DONE]\n\n"

    def chat_completion_response(
        self,
        request_output: RequestOutput,
        request_id: str,
    ) -> Union[ErrorResponse, ChatCompletionResponse]:

        model_name = self.model_name
        created_time = int(time.time())
        choices: List[ChatCompletionResponseChoice] = []

        role = self.response_role
        for output in request_output.outputs:
            message = ChatMessage(role=role, content=output.text)

            choice_data = ChatCompletionResponseChoice(
                index=output.index,
                message=message,
                finish_reason=output.finish_reason,
                # TODO: support logprobs
                logprobs=None,
                stop_reason=None,
            )
            choices.append(choice_data)

        # TODO: prompt tokens, etc.
        num_prompt_tokens = len(request_output.prompt_token_ids)
        num_generated_tokens = sum(len(output.token_ids) for output in request_output.outputs)
        usage = UsageInfo(
            prompt_tokens=num_prompt_tokens,
            completion_tokens=num_generated_tokens,
            total_tokens=num_prompt_tokens + num_generated_tokens,
        )
        response = ChatCompletionResponse(
            id=request_id,
            created=created_time,
            model=model_name,
            choices=choices,
            usage=usage,
            # TODO: support logprobs
            prompt_logprobs=None,
        )

        return response
