"""Sealed error hierarchy for Claude Code SDK."""


class ClaudeSDKError(Exception):
    """Base exception for all Claude SDK errors.

    Provides a common base class for all exceptions raised by the SDK,
    enabling users to catch all SDK-related errors in a single except clause.
    """

    pass


class ParseError(ClaudeSDKError):
    """Exception raised when parsing JSONL session files fails.

    This error is raised when:
    - Session files cannot be opened or read
    - Session directories are inaccessible
    - Critical parsing errors occur that prevent processing

    Note: Individual malformed records within a file are logged as warnings
    and do not raise this exception - this is reserved for file-level errors.
    """

    pass


class ValidationError(ClaudeSDKError):
    """Exception raised when data validation fails.

    This error indicates that data does not conform to expected schemas
    or contains invalid values that cannot be processed.
    """

    pass


class SessionError(ClaudeSDKError):
    """Exception raised when session processing fails.

    This error is raised when session reconstruction, metadata calculation,
    or other session-level operations cannot be completed.
    """

    pass
