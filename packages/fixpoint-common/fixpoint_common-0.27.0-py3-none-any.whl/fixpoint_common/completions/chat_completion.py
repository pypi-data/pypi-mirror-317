"""
This module contains the ChatCompletion class, which wraps a completion with a Fixpoint completion.
"""

__all__ = [
    "ChatCompletion",
    "ChatCompletionMessage",
    "ChatCompletionMessageParam",
    "ChatCompletionChunk",
    "CompletionUsage",
]

import json
from typing import Any, Optional, List, Literal, Type, TypeVar, Generic
from pydantic import Field, BaseModel, PrivateAttr
from openai.types.completion_usage import CompletionUsage
from openai.types.chat import ChatCompletionChunk
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.chat_completion import (
    ChatCompletion as OpenAIChatCompletion,
    Choice,
)
from openai.types.chat.chat_completion_message import ChatCompletionMessage

T = TypeVar("T", bound=BaseModel)
Tinner = TypeVar("Tinner", bound=BaseModel)


def _raw_set_attr(obj: Any, name: str, value: Any) -> None:
    """
    Set an attribute on an object without triggering any of the pydantic logic.
    """
    object.__setattr__(obj, name, value)


class ChatCompletion(OpenAIChatCompletion, Generic[T]):
    """
    A class that wraps a completion with a Fixpoint completion.
    """

    # TODO(jakub): This is a workaround to have this work with Pydantic.
    # We should make this field private.
    _original_completion: OpenAIChatCompletion = PrivateAttr()
    fixp: "ChatCompletion.Fixp[T]" = Field(exclude=True)

    class Fixp(BaseModel, Generic[Tinner]):
        """
        A class that represents a Fixpoint completion.
        """

        structured_output: Optional[Tinner]

    def __init__(
        self,
        *,
        # these are from the parent class
        id: str,  # pylint: disable=redefined-builtin
        choices: List[Choice],
        created: int,
        model: str,
        object: Literal["chat.completion"],  # pylint: disable=redefined-builtin
        system_fingerprint: Optional[str] = None,
        usage: Optional[CompletionUsage] = None,
        service_tier: Optional[Literal["scale", "default"]] = None,
        # we added these
        structured_output: Optional[T] = None
    ) -> None:

        orig_completion = OpenAIChatCompletion(
            id=id,
            choices=choices,
            created=created,
            model=model,
            object=object,
            system_fingerprint=system_fingerprint,
            service_tier=service_tier,
            usage=usage,
        )
        fixp = ChatCompletion.Fixp[T](structured_output=structured_output)
        super().__init__(
            id=id,
            choices=choices,
            created=created,
            model=model,
            object=object,
            system_fingerprint=system_fingerprint,
            usage=usage,
            # mypy type checker doesn't like this
            fixp=fixp.model_dump(),  # type: ignore[call-arg]
        )
        _raw_set_attr(self, "_original_completion", orig_completion)
        _raw_set_attr(self, "fixp", fixp)

    @classmethod
    def from_original_completion(
        cls,
        original_completion: OpenAIChatCompletion,
        structured_output: Optional[T] = None,
    ) -> "ChatCompletion[T]":
        """
        Create a new ChatCompletion from an original completion.
        """
        return cls(
            id=original_completion.id,
            choices=original_completion.choices,
            created=original_completion.created,
            model=original_completion.model,
            object=original_completion.object,
            system_fingerprint=original_completion.system_fingerprint,
            usage=original_completion.usage,
            structured_output=structured_output,
        )

    def serialize_json(self) -> str:
        """Serialize the ChatCompletion to a JSON string"""
        dumped = self._original_completion.model_dump(mode="json")
        sout = self.fixp.structured_output
        sout_str = None
        if sout:
            sout_str = sout.model_dump(mode="json")
        dumped["fixp"] = {"structured_output": sout_str}
        return json.dumps(dumped)

    @classmethod
    def deserialize_json(
        cls,
        json_string: str,
        response_model: Optional[Type[T]] = None,
    ) -> "ChatCompletion[T]":
        """Load a JSON string into a ChatCompletion object"""
        loaded = json.loads(json_string)
        fixploaded = loaded["fixp"]
        del loaded["fixp"]

        orig_completion = OpenAIChatCompletion.model_validate(loaded)
        if response_model:
            structured_output = response_model.model_validate(
                fixploaded["structured_output"]
            )
        else:
            structured_output = None

        return cls.from_original_completion(orig_completion, structured_output)

    def __getattr__(self, name: str) -> Any:
        # Forward attribute access to the underlying client
        return getattr(self._original_completion, name)
