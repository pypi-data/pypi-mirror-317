import asyncio
from asyncio import FIRST_COMPLETED, ensure_future
import contextlib
from typing import (
    AsyncGenerator,
    Awaitable,
    Callable,
    List,
    Optional,
    Tuple,
    TypedDict,
    TypeVar,
    Union,
)
import uuid

from fastapi import HTTPException, Request
from jinja2 import Template
import orjson
from pydantic import BaseModel
from transformers import PreTrainedTokenizer, PreTrainedTokenizerFast
from typing_extensions import Type

T = TypeVar("T")

# TODO: Add MistralTokenizer
AnyTokenizer = Union[PreTrainedTokenizer, PreTrainedTokenizerFast]


def random_uuid() -> str:
    return str(uuid.uuid4().hex)


class ConversationMessage(TypedDict):
    role: str
    content: str


def apply_chat_template(
    messages: List[ConversationMessage],
    chat_template: Template,
    tokenizer: AnyTokenizer,
) -> str:
    # XXX: we must upgrade transformers v4.34 or higher to use chat template support from tokenizers.
    return chat_template.render(
        messages=messages, add_generation_prompt=True, **tokenizer.special_tokens_map
    )


async def merge_async_iterators(
    *iterators: AsyncGenerator[T, None],
    is_cancelled: Optional[Callable[[], Awaitable[bool]]] = None,
) -> AsyncGenerator[Tuple[int, T], None]:
    """Merge multiple asynchronous iterators into a single iterator.

    This method handle the case where some iterators finish before others.
    When it yields, it yields a tuple (i, item) where i is the index of the
    iterator that yields the item.

    It also optionally polls a provided function at least once per second
    to check for client cancellation.
    """

    # Can use anext() in python >= 3.10
    awaits = {ensure_future(pair[1].__anext__()): pair for pair in enumerate(iterators)}
    timeout = None if is_cancelled is None else 1
    try:
        while awaits:
            done, pending = await asyncio.wait(
                awaits.keys(), return_when=FIRST_COMPLETED, timeout=timeout
            )
            if is_cancelled is not None and await is_cancelled():
                raise asyncio.CancelledError("client cancelled")
            for d in done:
                pair = awaits.pop(d)
                try:
                    item = await d
                    i, it = pair
                    awaits[ensure_future(it.__anext__())] = pair
                    yield i, item
                except StopAsyncIteration:
                    pass
    finally:
        # Cancel any remaining iterators
        for f, (_, it) in awaits.items():
            with contextlib.suppress(BaseException):
                f.cancel()
                await it.aclose()


BM = TypeVar("BM", bound=BaseModel)


async def parse_request(raw_request: Request, request_cls: Type[BM]) -> BM:
    if "application/json" not in raw_request.headers.get("Content-Type", ""):
        raise HTTPException(status_code=415, detail="Content-Type must be application/json")
    try:
        body = await raw_request.body()
        data = orjson.loads(body)
        request = request_cls.parse_obj(data)
        return request
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
