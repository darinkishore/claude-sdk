"""Message class for Claude Code conversations.

This module provides the Message class, which represents individual messages
in a Claude Code conversation, including user inputs and assistant responses.
"""

from .models import (
    MessageRecord as _MessageRecord,
)
from .models import (
    TextBlock,
    ToolUseBlock,
)


class Message(_MessageRecord):
    """Individual message in a Claude Code conversation.

    This class represents a single message in a Claude Code conversation,
    with properties for accessing message content, role, cost, and other
    attributes. It inherits from the internal MessageRecord model but
    provides a simplified interface for common operations.

    Args:
        All arguments from MessageRecord

    Properties:
        role: Role of the message sender ("user" or "assistant")
        text: Text content of the message
        cost: Cost of the message in USD
        is_sidechain: Whether this message is part of a sidechain
        timestamp: When the message was sent
        uuid: Unique message identifier
        parent_uuid: Parent message UUID for threading
        tools: List of tools used in this message

    Example:
        ```python
        from claude_sdk import load

        session = load("conversation.jsonl")
        for message in session.messages:
            print(f"{message.role}: {message.text}")
            if message.cost:
                print(f"Cost: ${message.cost:.4f}")
            if message.is_sidechain:
                print("(sidechain)")
        ```
    """

    @property
    def role(self) -> str:
        """Role of the message sender ("user" or "assistant").

        Returns:
            str: Message role
        """
        return self.message.role

    @property
    def text(self) -> str:
        """Text content of the message.

        For messages with multiple content blocks, this returns only the text portions
        concatenated together, omitting tool blocks and other non-text content.

        Returns:
            str: Text content of the message
        """
        text_parts: list[str] = []
        for block in self.message.content:
            if isinstance(block, TextBlock):
                text_parts.append(block.text)
        return "\n".join(text_parts)

    @property
    def cost(self) -> float | None:
        """Cost of the message in USD.

        Returns:
            Optional[float]: Message cost if available, None otherwise
        """
        return self.cost_usd

    @property
    def tools(self) -> list[str]:
        """List of tools used in this message.

        Returns:
            List[str]: Names of tools used in this message
        """
        tools: list[str] = []
        for block in self.message.content:
            if isinstance(block, ToolUseBlock):
                tools.append(block.name)
        return tools

    @classmethod
    def from_message_record(cls, record: _MessageRecord) -> "Message":
        """Create a Message from a MessageRecord instance.

        Args:
            record: MessageRecord instance to convert

        Returns:
            Message: New Message instance with the same data
        """
        # Convert using model_dump and model_validate to preserve all data
        return cls.model_validate(record.model_dump())

    def get_tool_blocks(self) -> list[ToolUseBlock]:
        """Get all tool use blocks in this message.

        Returns:
            List[ToolUseBlock]: List of tool use blocks
        """
        return [block for block in self.message.content if isinstance(block, ToolUseBlock)]
