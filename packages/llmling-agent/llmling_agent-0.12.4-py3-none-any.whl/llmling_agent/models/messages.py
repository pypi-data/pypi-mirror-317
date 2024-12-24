"""Message and token usage models."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Literal, TypedDict
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, Field
from typing_extensions import TypeVar


T = TypeVar("T", str, BaseModel, default=str)


class TokenUsage(TypedDict):
    """Token usage statistics from model responses."""

    total: int
    """Total tokens used"""
    prompt: int
    """Tokens used in the prompt"""
    completion: int
    """Tokens used in the completion"""


@dataclass(frozen=True)
class TokenAndCostResult:
    """Combined token and cost tracking."""

    token_usage: TokenUsage
    """Token counts for prompt and completion"""
    cost_usd: float
    """Total cost in USD"""


class MessageMetadata(BaseModel):
    """Metadata for chat messages."""

    timestamp: datetime = Field(default_factory=datetime.now)
    """When the message was created."""

    model: str | None = Field(default=None)
    """Name of the model used to generate this message."""

    token_usage: TokenUsage | None = Field(default=None)
    """Token usage statistics if available."""

    cost: float | None = Field(default=None)
    """Cost in USD for generating this message."""

    tool: str | None = Field(default=None)
    """Name of tool if this message represents a tool interaction."""

    # Web UI specific fields
    avatar: str | None = Field(default=None)
    """URL or path to avatar image for UI display."""

    name: str | None = Field(default=None)
    """Display name for the message sender in UI."""

    tool_args: dict[str, Any] | None = None
    """Arguments passed to tool for UI display."""

    tool_result: Any | None = None
    """Result returned by tool for UI display."""

    model_config = ConfigDict(frozen=True)


class ChatMessage[T](BaseModel):
    """Common message format for all UI types.

    Generically typed with: ChatMessage[Type of Content]
    The type can either be str or a BaseModel subclass.
    """

    content: T
    """Message content, typed as T (either str or BaseModel)."""

    model: str | None = Field(default=None)
    """Name of the model that generated this message."""

    role: Literal["user", "assistant", "system"]
    """Role of the message sender (user/assistant/system)."""

    metadata: MessageMetadata = Field(default_factory=MessageMetadata)
    """Additional metadata about the message (timing, costs, tool usage, etc)."""

    timestamp: datetime = Field(default_factory=datetime.now)
    """When this message was created."""

    token_usage: TokenUsage | None = Field(default=None)
    """Token usage for this specific message if available."""

    message_id: str = Field(default_factory=lambda: str(uuid4()))
    """Unique identifier for this message."""

    model_config = ConfigDict(frozen=True)

    def _get_content_str(self) -> str:
        """Get string representation of content."""
        match self.content:
            case str():
                return self.content
            case BaseModel():
                return self.content.model_dump_json(indent=2)
            case _:
                msg = f"Unexpected content type: {type(self.content)}"
                raise ValueError(msg)

    def to_gradio_format(self) -> tuple[str | None, str | None]:
        """Convert to Gradio chatbot format."""
        content_str = self._get_content_str()
        match self.role:
            case "user":
                return (content_str, None)
            case "assistant":
                return (None, content_str)
            case "system":
                return (None, f"System: {content_str}")
