# Adapted from
# https://github.com/vllm-project/vllm/blob/4ef41b84766670c1bd8079f58d35bf32b5bcb3ab/vllm/entrypoints/openai/protocol.py
import time
from typing import Dict, List, Literal, Optional, Union

from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel, ConfigDict, Field

from furiosa_llm.api import SamplingParams
from furiosa_llm.server.utils import random_uuid


class OpenAIBaseModel(BaseModel):
    # OpenAI API does not allow extra fields
    model_config = ConfigDict(extra="forbid")


class UsageInfo(OpenAIBaseModel):
    prompt_tokens: int = 0
    total_tokens: int = 0
    completion_tokens: Optional[int] = 0


class StreamOptions(OpenAIBaseModel):
    include_usage: Optional[bool] = True
    continuous_usage_stats: Optional[bool] = True


class ChatCompletionRequest(OpenAIBaseModel):
    messages: List[ChatCompletionMessageParam]
    model: str
    max_tokens: Optional[int] = None
    n: Optional[int] = 1
    temperature: Optional[float] = 1.0
    stream: Optional[bool] = False
    # XXX: stream_options has no effect in the current implementation
    stream_options: Optional[StreamOptions] = None
    top_p: Optional[float] = 1.0
    best_of: Optional[int] = None
    use_beam_search: bool = False
    top_k: int = -1
    min_p: float = 0.0
    length_penalty: float = 1.0
    early_stopping: bool = False
    min_tokens: int = 0
    add_generation_prompt: bool = True

    def to_sampling_params(self) -> SamplingParams:
        return SamplingParams.from_optional(
            n=self.n,
            best_of=self.best_of,
            temperature=self.temperature,
            top_p=self.top_p,
            top_k=self.top_k,
            use_beam_search=self.use_beam_search,
            length_penalty=self.length_penalty,
            early_stopping=self.early_stopping,
            max_tokens=self.max_tokens,
            min_tokens=self.min_tokens,
        )


class CompletionRequest(OpenAIBaseModel):
    model: str
    prompt: Union[List[int], List[List[int]], str, List[str]]
    best_of: Optional[int] = 1
    max_tokens: Optional[int] = 16
    n: int = 1
    temperature: Optional[float] = 1.0
    top_p: Optional[float] = 1.0

    stream: Optional[bool] = False
    # XXX: stream_options has no effect in the current implementation
    stream_options: Optional[StreamOptions] = None
    use_beam_search: bool = False
    top_k: int = -1
    min_p: float = 0.0
    length_penalty: float = 1.0
    early_stopping: bool = False
    min_tokens: int = 0

    def to_sampling_params(self) -> SamplingParams:
        return SamplingParams.from_optional(
            n=self.n,
            best_of=self.best_of,
            temperature=self.temperature,
            top_p=self.top_p,
            top_k=self.top_k,
            use_beam_search=self.use_beam_search,
            length_penalty=self.length_penalty,
            early_stopping=self.early_stopping,
            max_tokens=self.max_tokens,
            min_tokens=self.min_tokens,
        )


class Logprob(OpenAIBaseModel):
    logprob: float
    rank: Optional[int] = None
    decoded_token: Optional[str] = None


class CompletionLogProbs(OpenAIBaseModel):
    text_offset: List[int] = Field(default_factory=list)
    token_logprobs: List[Optional[float]] = Field(default_factory=list)
    tokens: List[str] = Field(default_factory=list)
    top_logprobs: List[Optional[Dict[str, float]]] = Field(default_factory=list)


class CompletionResponseChoice(OpenAIBaseModel):
    index: int
    text: str
    logprobs: Optional[CompletionLogProbs] = None
    finish_reason: Optional[str] = None
    stop_reason: Optional[Union[int, str]] = Field(
        default=None,
        description=(
            "The stop string or token id that caused the completion "
            "to stop, None if the completion finished for some other reason "
            "including encountering the EOS token"
        ),
    )
    prompt_logprobs: Optional[List[Optional[Dict[int, Logprob]]]] = None


class CompletionResponse(OpenAIBaseModel):
    id: str = Field(default_factory=lambda: f"cmpl-{random_uuid()}")
    object: str = "text_completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[CompletionResponseChoice]
    usage: UsageInfo


class CompletionResponseStreamChoice(OpenAIBaseModel):
    index: int
    text: str
    logprobs: Optional[CompletionLogProbs] = None
    finish_reason: Optional[str] = None
    stop_reason: Optional[Union[int, str]] = Field(
        default=None,
        description=(
            "The stop string or token id that caused the completion "
            "to stop, None if the completion finished for some other reason "
            "including encountering the EOS token"
        ),
    )


class CompletionStreamResponse(OpenAIBaseModel):
    id: str = Field(default_factory=lambda: f"cmpl-{random_uuid()}")
    object: str = "text_completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[CompletionResponseStreamChoice]
    usage: Optional[UsageInfo] = Field(default=None)


class EmbeddingResponseData(OpenAIBaseModel):
    index: int
    object: str = "embedding"
    embedding: Union[List[float], str]


class EmbeddingResponse(OpenAIBaseModel):
    id: str = Field(default_factory=lambda: f"cmpl-{random_uuid()}")
    object: str = "list"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    data: List[EmbeddingResponseData]
    usage: UsageInfo


class FunctionCall(OpenAIBaseModel):
    name: str
    arguments: str


class ToolCall(OpenAIBaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-tool-{random_uuid()}")
    type: Literal["function"] = "function"
    function: FunctionCall


class ChatMessage(OpenAIBaseModel):
    role: str
    content: str
    tool_calls: List[ToolCall] = Field(default_factory=list)


class ChatCompletionLogProb(OpenAIBaseModel):
    token: str
    logprob: float = -9999.0
    bytes: Optional[List[int]] = None


class ChatCompletionLogProbsContent(ChatCompletionLogProb):
    top_logprobs: List[ChatCompletionLogProb] = Field(default_factory=list)


class ChatCompletionLogProbs(OpenAIBaseModel):
    content: Optional[List[ChatCompletionLogProbsContent]] = None


class ChatCompletionResponseChoice(OpenAIBaseModel):
    index: int
    message: ChatMessage
    logprobs: Optional[ChatCompletionLogProbs] = None
    finish_reason: Optional[str] = None
    stop_reason: Optional[Union[int, str]] = None


class ChatCompletionResponse(OpenAIBaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{random_uuid()}")
    object: Literal["chat.completion"] = "chat.completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[ChatCompletionResponseChoice]
    usage: UsageInfo
    prompt_logprobs: Optional[List[Optional[Dict[int, Logprob]]]] = None


class DeltaMessage(OpenAIBaseModel):
    role: Optional[str] = None
    content: Optional[str] = None
    tool_calls: List[ToolCall] = Field(default_factory=list)


class ChatCompletionResponseStreamChoice(OpenAIBaseModel):
    index: int
    delta: DeltaMessage
    logprobs: Optional[ChatCompletionLogProbs] = None
    finish_reason: Optional[str] = None
    stop_reason: Optional[Union[int, str]] = None


class ChatCompletionStreamResponse(OpenAIBaseModel):
    id: str = Field(default_factory=lambda: f"chatcmpl-{random_uuid()}")
    object: Literal["chat.completion.chunk"] = "chat.completion.chunk"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[ChatCompletionResponseStreamChoice]
    usage: Optional[UsageInfo] = Field(default=None)


class ErrorResponse(OpenAIBaseModel):
    object: str = "error"
    message: str
    type: str
    param: Optional[str] = None
    code: int
