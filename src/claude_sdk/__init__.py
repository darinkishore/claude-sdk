"""Claude Code SDK - Typed Python wrapper for Claude Code CLI sessions.

This SDK provides a clean, intuitive interface for parsing and analyzing Claude Code
JSONL session files. It allows you to load session data, access messages, and analyze
costs, tool usage, and conversation patterns.

Basic usage:
```python
from claude_sdk import load, Session

# Load a session from a JSONL file
session = load("conversation.jsonl")

# Access session properties
print(f"Session ID: {session.session_id}")
print(f"Total cost: ${session.total_cost:.4f}")
print(f"Tools used: {session.tools_used}")
print(f"Messages: {len(session.messages)}")

# Iterate through messages
for msg in session.messages:
    print(f"{msg.role}: {msg.text}")
    if msg.cost:
        print(f"Cost: ${msg.cost:.4f}")
```

For finding session files:
```python
from claude_sdk import find_sessions

# Find all sessions in ~/.claude/projects/
session_paths = find_sessions()

# Find sessions in a specific directory
session_paths = find_sessions("/path/to/sessions")
```
"""

from pathlib import Path

from .errors import ClaudeSDKError, ParseError
from .message import Message
from .models import Role, SessionMetadata, TextBlock, ThinkingBlock, ToolExecution, ToolUseBlock
from .parser import discover_sessions, parse_complete_session
from .session import Session

__version__ = "0.1.0"


def load(file_path: str | Path) -> Session:
    """Load a Claude Code session from a JSONL file.

    This function parses a Claude Code session file and returns a Session object
    with all messages, metadata, and tool usage information.

    Args:
        file_path: Path to the JSONL session file (can be string or Path)

    Returns:
        Session: Complete session with all messages and metadata

    Raises:
        ParseError: If the file cannot be parsed
        FileNotFoundError: If the file does not exist

    Example:
        ```python
        from claude_sdk import load

        # Load a session
        session = load("conversation.jsonl")

        # Access session properties
        print(f"Session ID: {session.session_id}")
        print(f"Total cost: ${session.total_cost:.4f}")
        print(f"Messages: {len(session.messages)}")
        ```
    """
    # Convert string path to Path object if needed
    if isinstance(file_path, str):
        file_path = Path(file_path)

    # Parse the session using the internal function
    parsed_session = parse_complete_session(file_path)

    # Convert to the public Session class
    return Session.from_parsed_session(parsed_session)


def find_sessions(base_path: str | Path | None = None) -> list[Path]:
    """Find Claude Code session files in a directory.

    This function discovers all Claude Code JSONL session files in the specified
    directory or in the default ~/.claude/projects/ directory.

    Args:
        base_path: Directory to search for session files. If not provided,
                   defaults to ~/.claude/projects/

    Returns:
        List[Path]: List of paths to JSONL session files

    Raises:
        ParseError: If the directory doesn't exist or can't be accessed

    Example:
        ```python
        from claude_sdk import find_sessions, load

        # Find all sessions in default directory
        session_paths = find_sessions()

        # Find sessions in a specific directory
        session_paths = find_sessions("/path/to/sessions")

        # Load the first session
        if session_paths:
            session = load(session_paths[0])
            print(f"Loaded session: {session.session_id}")
        ```
    """
    # Convert string path to Path object if needed
    if base_path is not None and isinstance(base_path, str):
        base_path = Path(base_path)

    # Use the internal discover_sessions function
    return discover_sessions(base_path)


# Type exports for static analysis
__all__ = [
    # Error handling
    "ClaudeSDKError",
    "Message",
    "ParseError",
    # Common model types
    "Role",
    # Main classes
    "Session",
    "SessionMetadata",
    "TextBlock",
    "ThinkingBlock",
    "ToolExecution",
    "ToolUseBlock",
    # Version
    "__version__",
    "find_sessions",
    # Core functions
    "load",
]
