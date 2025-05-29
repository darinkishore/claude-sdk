"""Pydantic data models for Claude Code SDK.

This module provides the foundational type system for parsing Claude Code JSONL session files.
All models are immutable (frozen=True) and use strict validation (extra='forbid').
"""

from datetime import datetime
from enum import Enum
from pathlib import Path
from uuid import UUID

from pydantic import BaseModel, ConfigDict

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


# Export all foundation types for public API
__all__ = [
    "ClaudeSDKBaseModel",
    "DateTimeType",
    "MessageType",
    "PathType",
    "Role",
    "StopReason",
    "UUIDType",
    "UserType",
]
