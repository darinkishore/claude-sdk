"""Session container for Claude Code sessions.

This module provides the Session class, which is the primary interface for
working with Claude Code session data. It contains messages, metadata, and
utility methods for analyzing session content.
"""

from datetime import timedelta

from .models import (
    MessageRecord as _MessageRecord,
)
from .models import (
    ParsedSession as _ParsedSession,
)


class Session(_ParsedSession):
    """Primary container for Claude Code session data.

    This class represents a complete Claude Code session, containing messages,
    conversation threading, tool usage information, and metadata. It provides
    properties for common analytics like cost and tool usage, and methods for
    exploring the session content.

    Args:
        session_id: Unique session identifier
        messages: List of message records from the session
        summaries: Optional summary records for the session
        conversation_tree: Tree structure of message relationships
        metadata: Aggregated session statistics
        tool_executions: Extracted tool execution records

    Properties:
        total_cost: Total USD cost of the session
        tools_used: Set of tool names used in the session
        duration: Total session duration from first to last message
        tool_costs: Cost breakdown by tool
        cost_by_turn: Cost breakdown by message turn

    Example:
        ```python
        from claude_sdk import load

        # Load a session
        session = load("conversation.jsonl")

        # Access session properties
        print(f"Session ID: {session.session_id}")
        print(f"Total cost: ${session.total_cost:.4f}")
        print(f"Tools used: {session.tools_used}")
        print(f"Messages: {len(session.messages)}")

        # Iterate through messages
        for msg in session.messages:
            print(f"{msg.role}: {msg.text}")
        ```
    """

    @property
    def total_cost(self) -> float:
        """Total cost of the session in USD.

        Returns:
            float: Total cost in USD
        """
        return self.metadata.total_cost

    @property
    def tools_used(self) -> set[str]:
        """Set of tool names used in this session.

        Returns:
            Set[str]: Names of all tools used in the session
        """
        return set(self.metadata.tool_usage_count.keys())

    @property
    def duration(self) -> timedelta | None:
        """Total duration of the session from first to last message.

        Returns:
            Optional[timedelta]: Session duration if timestamps available, None otherwise
        """
        return self.metadata.session_duration

    @property
    def tool_costs(self) -> dict[str, float]:
        """Cost breakdown by tool.

        Returns:
            Dict[str, float]: Mapping of tool names to their total cost
        """
        # Use the tool_usage_count from metadata to create dictionary
        tool_costs: dict[str, float] = {}

        # Initialize all tools with 0.0 cost
        for tool_name in self.tools_used:
            tool_costs[tool_name] = 0.0

        # Simple approximation - distribute costs evenly across tools
        if self.tools_used and self.total_cost > 0:
            avg_tool_cost = self.total_cost / len(self.tools_used)
            for tool_name in self.tools_used:
                # Weight by usage count
                usage_count = self.metadata.tool_usage_count.get(tool_name, 0)
                if usage_count > 0:
                    tool_costs[tool_name] = (
                        avg_tool_cost * usage_count / sum(self.metadata.tool_usage_count.values())
                    )

        return tool_costs

    @property
    def cost_by_turn(self) -> list[float]:
        """Cost breakdown by message turn.

        Returns:
            List[float]: List of costs per message, in message order
        """
        return [
            message.cost_usd if message.cost_usd is not None else 0.0 for message in self.messages
        ]

    @classmethod
    def from_parsed_session(cls, parsed_session: _ParsedSession) -> "Session":
        """Create a Session from a ParsedSession instance.

        Args:
            parsed_session: ParsedSession instance to convert

        Returns:
            Session: New Session instance with the same data
        """
        return cls(
            session_id=parsed_session.session_id,
            messages=parsed_session.messages,
            summaries=parsed_session.summaries,
            conversation_tree=parsed_session.conversation_tree,
            metadata=parsed_session.metadata,
            tool_executions=parsed_session.tool_executions,
        )

    @classmethod
    def from_message_records(
        cls,
        messages: list[_MessageRecord],
        session_id: str | None = None,
        summaries: list[str] | None = None,
    ) -> "Session":
        """Assemble a complete Session from MessageRecord list.

        Args:
            messages: List of MessageRecord objects to assemble into a session
            session_id: Override session ID (auto-detected from messages if None)
            summaries: Optional summary records for the session

        Returns:
            Session: Complete session with threading, metadata, and tool executions

        Raises:
            ValueError: If messages list is empty or session_id cannot be determined
        """
        parsed_session = _ParsedSession.from_message_records(
            messages=messages,
            session_id=session_id,
            summaries=summaries,
        )
        return cls.from_parsed_session(parsed_session)

    def get_main_chain(self) -> list[_MessageRecord]:
        """Get only the main conversation chain (excluding sidechains).

        Returns:
            List[MessageRecord]: List of messages in the main conversation chain
        """
        return [msg for msg in self.messages if not msg.is_sidechain]

    def get_messages_by_role(self, role: str) -> list[_MessageRecord]:
        """Get messages with a specific role.

        Args:
            role: Role to filter by ("user" or "assistant")

        Returns:
            List[MessageRecord]: List of messages with the specified role
        """
        return [msg for msg in self.messages if msg.message.role == role]
