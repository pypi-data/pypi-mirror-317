from typing import List, Optional


class CompletionOutput:
    """The output data of one completion output of a request.

    Args:
        index: The index of the output in the request.
        text: The generated output text.
        token_ids: The token IDs of the generated output text.
        finish_reason: The reason why the sequence is finished.
    """

    def __init__(
        self,
        index: int,
        text: str,
        token_ids: List[int],
        finish_reason: Optional[str] = None,
    ) -> None:
        self.index = index
        self.text = text
        self.token_ids = token_ids
        self.finish_reason = finish_reason

    def __repr__(self) -> str:
        return (
            f"CompletionOutput(index={self.index}, "
            f"text={self.text!r}, "
            f"token_ids={self.token_ids}, "
            f"finish_reason={self.finish_reason})"
        )


class RequestOutput:
    def __init__(
        self,
        request_id: str,
        prompt: str,
        prompt_token_ids: List[int],
        outputs: List[CompletionOutput],
        finished: bool,
    ) -> None:
        self.request_id = request_id
        self.prompt = prompt
        self.prompt_token_ids = prompt_token_ids
        self.outputs = outputs
        self.finished = finished

    def __repr__(self) -> str:
        return (
            f"RequestOutput(request_id={self.request_id}, "
            f"prompt={self.prompt!r}, "
            f"prompt_token_ids={self.prompt_token_ids}, "
            f"outputs={self.outputs}, "
            f"finished={self.finished})"
        )
