from argparse import Namespace

from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import ORJSONResponse, Response, StreamingResponse
import uvicorn

from furiosa_llm.server.models import load_llm_from_args
from furiosa_llm.server.protocol import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    CompletionRequest,
    CompletionResponse,
    ErrorResponse,
)
from furiosa_llm.server.serving_chat import OpenAIServingChat
from furiosa_llm.server.serving_completions import OpenAIServingCompletion
from furiosa_llm.server.utils import parse_request

router = APIRouter()

openai_serving_completion: OpenAIServingCompletion
openai_serving_chat: OpenAIServingChat


@router.get("/health")
async def health() -> Response:
    """Health check."""
    # TODO: reflect LLM engine's health
    return Response(status_code=200)


@router.post("/v1/completions")
async def create_completion(raw_request: Request):
    request = await parse_request(raw_request, CompletionRequest)
    generator = await openai_serving_completion.create_completion(request, raw_request)
    if isinstance(generator, ErrorResponse):
        return ORJSONResponse(content=generator.model_dump(), status_code=generator.code)
    elif isinstance(generator, CompletionResponse):
        return ORJSONResponse(content=generator.model_dump())

    return StreamingResponse(content=generator, media_type="text/event-stream")


@router.post("/v1/chat/completions")
async def create_chat_completion(raw_request: Request):
    request = await parse_request(raw_request, ChatCompletionRequest)
    generator = await openai_serving_chat.create_chat_completion(request, raw_request)
    if isinstance(generator, ErrorResponse):
        return ORJSONResponse(content=generator.model_dump(), status_code=generator.code)
    elif isinstance(generator, ChatCompletionResponse):
        return ORJSONResponse(content=generator.model_dump())

    return StreamingResponse(content=generator, media_type="text/event-stream")


def init_app(
    args: Namespace,
) -> FastAPI:
    app = FastAPI()
    app.include_router(router)
    llm = load_llm_from_args(args)

    # Hack to pre-warm tokenizer
    llm.tokenizer("hello world")

    assert llm.is_generative_model
    # FIXME: model_max_seq_len is the "theoretical" maximum sequence length that the model can handle,
    # but we need the maximum decode bucket size that user provided.
    # TODO - make LLM.max_seq_len_to_capture an attribute and use it
    model_max_seq_len = llm.model_max_seq_len

    if args.chat_template is not None:
        try:
            chat_template = open(args.chat_template).read()
        except Exception as e:
            raise ValueError(f"Error in reading chat template file: {e}")
    else:
        try:
            chat_template = llm.tokenizer.get_chat_template()
        except Exception as e:
            raise ValueError(
                f"Failed to load chat template from tokenizer: {e}. Please specify a chat template using the --chat-template option."
            )

    global openai_serving_completion
    global openai_serving_chat
    openai_serving_completion = OpenAIServingCompletion(llm, model_max_seq_len)
    openai_serving_chat = OpenAIServingChat(
        llm, model_max_seq_len, chat_template, args.response_role
    )

    return app


def run_server(args, **uvicorn_kwargs) -> None:
    app = init_app(args)
    uvicorn.run(app, host=args.host, port=args.port, **uvicorn_kwargs)
