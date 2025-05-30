"""JSONL parsing and session reconstruction for Claude Code SDK."""

import json
import logging
from collections.abc import Iterator
from pathlib import Path

from pydantic import ValidationError

from .errors import ParseError
from .models import MessageRecord, ParsedSession

logger = logging.getLogger(__name__)


def discover_sessions(base_path: Path | None = None) -> list[Path]:
    """Discover Claude Code session files in the user's projects directory.

    Args:
        base_path: Base directory to search. Defaults to ~/.claude/projects/

    Returns:
        List of paths to JSONL session files

    Raises:
        ParseError: If base directory doesn't exist or isn't accessible
    """
    if base_path is None:
        base_path = Path.home() / ".claude" / "projects"

    if not base_path.exists():
        raise ParseError(f"Projects directory not found: {base_path}")

    if not base_path.is_dir():
        raise ParseError(f"Projects path is not a directory: {base_path}")

    try:
        # Find all .jsonl files recursively
        session_files = list(base_path.rglob("*.jsonl"))
        logger.info(f"Found {len(session_files)} JSONL files in {base_path}")
        return session_files
    except (OSError, PermissionError) as e:
        raise ParseError(f"Failed to access projects directory {base_path}: {e}") from e


def parse_jsonl_file(file_path: Path) -> Iterator[MessageRecord]:
    """Parse a JSONL file line-by-line into MessageRecord objects.

    Args:
        file_path: Path to the JSONL file to parse

    Yields:
        MessageRecord objects for each valid line

    Raises:
        ParseError: If file cannot be opened or read
    """
    if not file_path.exists():
        raise ParseError(f"Session file not found: {file_path}")

    if not file_path.is_file():
        raise ParseError(f"Session path is not a file: {file_path}")

    try:
        with file_path.open("r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                try:
                    # Parse JSON line
                    json_data = json.loads(line)

                    # Convert to MessageRecord using Pydantic
                    message_record = MessageRecord.model_validate(json_data)
                    yield message_record

                except json.JSONDecodeError as e:
                    logger.warning(f"Invalid JSON at {file_path}:{line_num}: {e}")
                    continue  # Skip malformed JSON lines

                except ValidationError as e:
                    logger.warning(f"Validation error at {file_path}:{line_num}: {e}")
                    continue  # Skip lines that don't match MessageRecord schema

                except Exception as e:
                    logger.error(f"Unexpected error at {file_path}:{line_num}: {e}")
                    continue  # Continue processing despite unexpected errors

    except (OSError, PermissionError) as e:
        raise ParseError(f"Failed to read session file {file_path}: {e}") from e


def parse_session_file(file_path: Path) -> list[MessageRecord]:
    """Parse a complete JSONL session file into a list of MessageRecord objects.

    Args:
        file_path: Path to the JSONL session file

    Returns:
        List of MessageRecord objects from the session

    Raises:
        ParseError: If file cannot be parsed
    """
    try:
        records = list(parse_jsonl_file(file_path))
        logger.info(f"Successfully parsed {len(records)} records from {file_path}")
        return records
    except ParseError:
        raise  # Re-raise ParseError as-is
    except Exception as e:
        raise ParseError(f"Failed to parse session file {file_path}: {e}") from e


class SessionParser:
    """High-level parser for Claude Code session files.

    Provides methods for discovering and parsing JSONL session files
    with comprehensive error handling and logging.
    """

    def __init__(self, base_path: Path | None = None):
        """Initialize the session parser.

        Args:
            base_path: Base directory for session discovery. Defaults to ~/.claude/projects/
        """
        self.base_path = base_path or Path.home() / ".claude" / "projects"

    def discover_sessions(self) -> list[Path]:
        """Discover all JSONL session files in the base path.

        Returns:
            List of paths to discovered session files
        """
        return discover_sessions(self.base_path)

    def parse_session(self, file_path: Path) -> list[MessageRecord]:
        """Parse a single JSONL session file.

        Args:
            file_path: Path to the session file

        Returns:
            List of MessageRecord objects from the session
        """
        return parse_session_file(file_path)

    def parse_all_sessions(self) -> dict[Path, list[MessageRecord]]:
        """Parse all discovered session files.

        Returns:
            Dictionary mapping file paths to lists of MessageRecord objects
        """
        session_files = self.discover_sessions()
        results: dict[Path, list[MessageRecord]] = {}

        for file_path in session_files:
            try:
                records = self.parse_session(file_path)
                results[file_path] = records
            except ParseError as e:
                logger.error(f"Failed to parse {file_path}: {e}")
                results[file_path] = []  # Empty list for failed sessions

        return results

    def parse_complete_session(self, file_path: Path) -> ParsedSession:
        """Parse a single JSONL session file into a complete ParsedSession.

        Args:
            file_path: Path to the session file

        Returns:
            ParsedSession: Complete session with threading, metadata, and tool executions
        """
        return parse_complete_session(file_path)


def parse_complete_session(file_path: Path) -> ParsedSession:
    """Parse a JSONL session file into a complete ParsedSession with threading and metadata.

    Args:
        file_path: Path to the JSONL session file

    Returns:
        ParsedSession: Complete session with conversation threading, metadata, and tool executions

    Raises:
        ParseError: If file cannot be parsed
    """
    try:
        # Parse raw message records
        message_records = parse_session_file(file_path)

        # Assemble into complete ParsedSession
        session = ParsedSession.from_message_records(message_records)

        logger.info(
            f"Successfully parsed session {session.session_id} with "
            f"{len(session.messages)} messages, "
            f"{len(session.tool_executions)} tool executions"
        )

        return session

    except ParseError:
        raise  # Re-raise ParseError as-is
    except Exception as e:
        raise ParseError(f"Failed to parse complete session from {file_path}: {e}") from e
