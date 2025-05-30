"""Pydantic data models for Claude Code SDK.

This module provides the foundational type system for parsing Claude Code JSONL session files.
All models are immutable (frozen=True) and use strict validation (extra='forbid').
"""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, PositiveFloat, PositiveInt

# Type aliases for common types
UUIDType = UUID
DateTimeType = datetime
PathType = Path


class UserType(str, Enum):
    """Type of user interaction in Claude Code sessions.

    Determines whether the interaction originated from an external user
    or internal system processes.
    """

    EXTERNAL = "external"  # External user interactions
    INTERNAL = "internal"  # Internal system interactions


class MessageType(str, Enum):
    """Type of message in a conversation.

    Distinguishes between user messages and assistant responses
    in the conversation flow.
    """

    USER = "user"  # User messages
    ASSISTANT = "assistant"  # Assistant responses


class Role(str, Enum):
    """Role in conversation context.

    Defines the role of the message sender in the conversation,
    corresponding to the 'role' field in JSONL records.
    """

    USER = "user"  # User role
    ASSISTANT = "assistant"  # Assistant role


class StopReason(str, Enum):
    """Reason why message generation stopped.

    Indicates the termination condition for assistant message generation,
    providing insight into conversation flow and token usage.
    """

    END_TURN = "end_turn"  # Natural conversation end
    MAX_TOKENS = "max_tokens"  # Token limit reached
    STOP_SEQUENCE = "stop_sequence"  # Stop sequence encountered


class ClaudeSDKBaseModel(BaseModel):
    """Base model class for all Claude SDK Pydantic models.

    Provides consistent configuration across all data models:
    - frozen=True: Makes models immutable after creation
    - extra='forbid': Prevents unexpected fields in input data

    This ensures type safety and catches configuration errors early.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")


class TextBlock(ClaudeSDKBaseModel):
    """Plain text content block.

    Represents regular text content within messages. This is the most
    common content block type in conversations.
    """

    type: Literal["text"] = "text"
    text: str


class ThinkingBlock(ClaudeSDKBaseModel):
    """Internal thinking/reasoning content block.

    Represents Claude's internal reasoning process that is made visible
    to users. Contains the thinking content and associated signature.
    """

    type: Literal["thinking"] = "thinking"
    thinking: str
    signature: str


class ToolUseBlock(ClaudeSDKBaseModel):
    """Tool usage content block.

    Represents a request to execute a tool with specific parameters.
    Contains tool identification and arbitrary input parameters.
    """

    type: Literal["tool_use"] = "tool_use"
    id: str
    name: str
    input: dict[str, Any]


class ToolResultBlock(ClaudeSDKBaseModel):
    """Tool execution result content block.

    Represents the result of a tool execution, including output content,
    error status, and correlation to the original tool use request.
    """

    type: Literal["tool_result"] = "tool_result"
    content: str
    is_error: bool = Field(alias="is_error")
    tool_use_id: str = Field(alias="tool_use_id")


class TokenUsage(ClaudeSDKBaseModel):
    """Token usage statistics for a message.

    Tracks input and output token consumption, including cache usage
    for performance optimization and cost calculation.
    """

    input_tokens: int = Field(ge=0, alias="input_tokens")
    cache_creation_input_tokens: int = Field(default=0, ge=0, alias="cache_creation_input_tokens")
    cache_read_input_tokens: int = Field(default=0, ge=0, alias="cache_read_input_tokens")
    output_tokens: int = Field(ge=0, alias="output_tokens")
    service_tier: str = Field(default="standard", alias="service_tier")


class ToolResult(ClaudeSDKBaseModel):
    """Tool execution result metadata.

    Contains tool execution results as specified in the technical specification,
    including basic execution data and optional metadata.
    """

    tool_use_id: str
    content: str
    stdout: str | None = None
    stderr: str | None = None
    interrupted: bool = False
    is_error: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


class Message(ClaudeSDKBaseModel):
    """Message content within a conversation record.

    Represents the actual message data including role, content blocks,
    model information, and token usage statistics.
    """

    id: str | None = None
    role: Role
    model: str | None = None
    content: list["MessageContentBlock"]
    stop_reason: StopReason | None = Field(default=None, alias="stop_reason")
    usage: TokenUsage | None = None


class MessageRecord(ClaudeSDKBaseModel):
    """Complete Claude Code JSONL message record.

    Maps directly to the JSONL structure with conversation threading,
    message content, tool execution results, and performance metrics.
    """

    parent_uuid: UUID | None = Field(default=None, alias="parentUuid")
    is_sidechain: bool = Field(alias="isSidechain")
    user_type: UserType = Field(alias="userType")
    cwd: PathType
    session_id: str = Field(alias="sessionId")
    version: str
    message_type: MessageType = Field(alias="type")
    message: Message
    uuid: UUID
    timestamp: DateTimeType

    # Optional performance and metadata fields
    cost_usd: PositiveFloat | None = Field(default=None, alias="costUSD")
    duration_ms: PositiveInt | None = Field(default=None, alias="durationMs")
    request_id: str | None = Field(default=None, alias="requestId")
    tool_use_result: str | ToolResult | None = Field(default=None, alias="toolUseResult")
    is_meta: bool | None = Field(default=None, alias="isMeta")


# Base type alias for content blocks (for isinstance checks)
ContentBlock = TextBlock | ThinkingBlock | ToolUseBlock | ToolResultBlock


# Type alias for message content (discriminated union - excludes ToolResultBlock per spec)
MessageContentBlock = TextBlock | ThinkingBlock | ToolUseBlock

# Type alias for all content blocks (includes ToolResultBlock)
MessageContentType = TextBlock | ThinkingBlock | ToolUseBlock | ToolResultBlock


# Export all foundation types for public API
__all__ = [
    "ClaudeSDKBaseModel",
    "ContentBlock",
    "DateTimeType",
    "Message",
    "MessageContentBlock",
    "MessageContentType",
    "MessageRecord",
    "MessageType",
    "PathType",
    "Role",
    "StopReason",
    "TextBlock",
    "ThinkingBlock",
    "TokenUsage",
    "ToolResult",
    "ToolResultBlock",
    "ToolUseBlock",
    "UUIDType",
    "UserType",
]
