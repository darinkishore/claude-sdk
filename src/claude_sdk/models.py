"""Pydantic data models for Claude Code SDK.

This module provides the foundational type system for parsing Claude Code JSONL session files.
All models are immutable (frozen=True) and use strict validation (extra='forbid').
"""

from datetime import datetime, timedelta
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


class SessionMetadata(ClaudeSDKBaseModel):
    """Session metadata with aggregated cost, token, and tool usage information.

    Aggregates data from all MessageRecords in a session to provide
    session-level analytics and cost tracking.
    """

    total_cost: float = Field(default=0.0, ge=0.0, description="Total USD cost for the session")
    total_messages: int = Field(default=0, ge=0, description="Count of all messages in the session")
    tool_usage_count: dict[str, int] = Field(
        default_factory=dict, description="Tool name to usage count mapping"
    )


class ToolExecution(ClaudeSDKBaseModel):
    """Tool execution record with timing and result information.

    Represents a single tool execution extracted from tool blocks,
    including input parameters, output results, and performance metrics.
    """

    tool_name: str = Field(description="Name of the executed tool")
    input: dict[str, Any] = Field(description="Tool input parameters")
    output: ToolResult = Field(description="Tool execution output/result")
    duration: timedelta = Field(description="Execution duration")
    timestamp: datetime = Field(description="When the tool was executed")


class ConversationTree(ClaudeSDKBaseModel):
    """Placeholder for future conversation threading implementation.

    Will contain conversation tree structure based on parent_uuid relationships
    for conversation threading support (planned for S03).
    """

    # Placeholder fields for future implementation
    pass


class ParsedSession(ClaudeSDKBaseModel):
    """Main session container with messages, metadata, and session information.

    Primary interface for complete session data, aggregating all parsed
    MessageRecords with session-level metadata and analytics.
    """

    session_id: str = Field(description="Unique session identifier")
    messages: list[MessageRecord] = Field(
        default_factory=list, description="All parsed messages in the session"
    )
    summaries: list[str] = Field(default_factory=list, description="Summary records if present")
    conversation_tree: ConversationTree = Field(
        default_factory=ConversationTree,
        description="Conversation tree structure (future threading support)",
    )
    metadata: SessionMetadata = Field(
        default_factory=SessionMetadata, description="Aggregated session statistics"
    )

    def validate_session_integrity(self) -> bool:
        """Validate session data integrity.

        Returns:
            bool: True if session data is valid, False otherwise
        """
        # Check if session_id is consistent across all messages
        if self.messages:
            expected_session_id = self.messages[0].session_id
            for message in self.messages:
                if message.session_id != expected_session_id:
                    return False

        # Check if metadata aggregations match actual message data
        expected_message_count = len(self.messages)
        return self.metadata.total_messages == expected_message_count

    def calculate_metadata(self) -> SessionMetadata:
        """Calculate session metadata from current messages.

        Returns:
            SessionMetadata: Calculated metadata based on current messages
        """
        total_cost = 0.0
        total_messages = len(self.messages)
        tool_usage_count: dict[str, int] = {}

        for message in self.messages:
            # Aggregate costs
            if message.cost_usd:
                total_cost += message.cost_usd

            # Count tool usage
            for content_block in message.message.content:
                if isinstance(content_block, ToolUseBlock):
                    tool_name = content_block.name
                    tool_usage_count[tool_name] = tool_usage_count.get(tool_name, 0) + 1

        return SessionMetadata(
            total_cost=total_cost, total_messages=total_messages, tool_usage_count=tool_usage_count
        )


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
    "ConversationTree",
    "DateTimeType",
    "Message",
    "MessageContentBlock",
    "MessageContentType",
    "MessageRecord",
    "MessageType",
    "ParsedSession",
    "PathType",
    "Role",
    "SessionMetadata",
    "StopReason",
    "TextBlock",
    "ThinkingBlock",
    "TokenUsage",
    "ToolExecution",
    "ToolResult",
    "ToolResultBlock",
    "ToolUseBlock",
    "UUIDType",
    "UserType",
]
