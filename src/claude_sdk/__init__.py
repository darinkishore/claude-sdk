"""Claude Code SDK - Typed Python wrapper for Claude Code CLI."""

__version__ = "0.1.0"

# Core exports will be added as we implement the modules
# from .models import (
#     SessionConfig,
#     ClaudeSession,
#     MessageRecord,
#     SummaryRecord,
#     ToolExecution,
#     ClaudeOutput,
#     ExecutionResult,
#     # Content types
#     TextBlock,
#     ThinkingBlock,
#     ToolUseBlock,
#     # Enums
#     Role,
#     MessageType,
#     StopReason,
#     UserType,
# )

# from .parser import (
#     SessionParser,
#     ParsedSession,
#     ConversationTree,
#     ConversationNode,
#     SessionMetadata,
# )

# from .executor import ClaudeExecutor
# from .errors import (
#     ClaudeSDKError,
#     ParseError,
#     ExecutionError,
#     SessionError,
#     ClaudeErrorCode,
# )

# Builder pattern
# from .parser import ClaudeSessionBuilder

# Convenience functions will be added later
# def parse_session(file_path: Union[str, Path]) -> ParsedSession:
#     """Parse a Claude Code session file."""
#     parser = SessionParser(file_path)
#     return parser.parse()

# Type exports for static analysis
__all__ = [
    "__version__",
    # Will be populated as modules are implemented
]
