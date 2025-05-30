# Claude SDK

> Typed Python SDK for parsing and analyzing Claude Code sessions

A clean, intuitive interface for working with Claude Code JSONL session files. Designed for CLI-based workflows, the SDK provides a simple API to access messages, analyze costs, and extract structured data from your Claude Code sessions.

## Features

- **Simple API**: `session = load("conversation.jsonl")` - that's it!
- **Project-Level Analysis**: Aggregate data across multiple sessions in a project
- **Session Analysis**: Easily access cost, tool usage, and performance metrics
- **Message Access**: Clean iteration through conversation messages
- **Type Safety**: Full typing with Pydantic models and basedpyright --strict
- **CLI-Friendly**: Rich docstrings with examples for `help()` discovery
- **Memory Efficient**: Optimized for large session files

## Installation

```bash
uv add claude-sdk
```

## Quick Start

```python
from claude_sdk import load, find_sessions, find_projects, load_project

# Load a session from a JSONL file
session = load("conversation.jsonl")

# Access session properties
print(f"Session ID: {session.session_id}")
print(f"Total cost: ${session.total_cost:.4f}")
print(f"Tools used: {', '.join(session.tools_used)}")
print(f"Messages: {len(session.messages)}")

# Load a complete project
project = load_project("apply-model")  # By project name
print(f"Project: {project.name}")
print(f"Total sessions: {project.total_sessions}")
print(f"Total cost: ${project.total_cost:.4f}")
print(f"Date range: {project.first_session_date} to {project.last_session_date}")

# Find sessions filtered by project
sessions = find_sessions(project="apply-model")
print(f"Found {len(sessions)} sessions in apply-model project")
```

## Data Model Hierarchy

The SDK provides a clean hierarchy: **Project** → **Session** → **Message** → **Tool**

### Project Object

A project represents a Claude Code project directory containing multiple sessions:

```python
project = load_project("apply-model")

# Properties
project.name                 # str - Human-readable project name
project.project_path         # Path - Full path to project directory
project.sessions             # list[Session] - All sessions in the project
project.total_sessions       # int - Number of sessions
project.total_cost           # float - Total cost across all sessions (USD)
project.tools_used           # set[str] - All unique tools used
project.tool_usage_count     # dict[str, int] - Tool name to usage count
project.first_session_date   # datetime | None - Earliest session start
project.last_session_date    # datetime | None - Latest session start
project.total_duration       # timedelta | None - Time span of project

# Example usage
print(f"Project: {project.name}")
print(f"Sessions: {project.total_sessions}")
print(f"Total cost: ${project.total_cost:.4f}")
print(f"Duration: {project.total_duration.days} days")

for tool, count in project.tool_usage_count.items():
    print(f"  {tool}: {count} uses")
```

### Session Object

A session represents a single conversation loaded from a JSONL file:

```python
session = load("conversation.jsonl")

# Core properties
session.session_id           # str - Unique session identifier
session.project_name         # str | None - Name of containing project
session.project_path         # Path | None - Path to containing project
session.messages             # list[Message] - All messages in order
session.metadata             # SessionMetadata - Session metadata
session.total_cost           # float - Total session cost (USD)
session.tools_used           # set[str] - Unique tools used
session.duration             # timedelta | None - Session duration

# Analysis properties
session.tool_costs           # dict[str, float] - Cost per tool
session.cost_by_turn         # list[float] - Cost per message turn
session.tool_executions      # list[ToolExecution] - All tool uses

# Metadata sub-properties
session.metadata.session_start      # datetime | None
session.metadata.session_end        # datetime | None
session.metadata.total_cost         # float
session.metadata.compute_time_ms    # int | None
session.metadata.message_count      # int
session.metadata.session_id         # str
```

### Message Object

Each message in a session contains the conversation content and metadata:

```python
for msg in session.messages:
    # Core properties
    msg.role                 # Role - "user" or "assistant" enum
    msg.text                 # str - Full message text content
    msg.content              # list[TextBlock | ToolUseBlock] - Content blocks
    msg.cost                 # float | None - Message cost if available
    msg.tools                # list[str] - Names of tools used

    # Metadata properties
    msg.uuid                 # str - Unique message identifier
    msg.parent_uuid          # str | None - Parent message UUID
    msg.timestamp            # datetime - Message creation time
    msg.is_sidechain         # bool - True if in a sidechain
    msg.model                # str | None - Model used (e.g. "claude-3-5-sonnet")
    msg.compute_time_ms      # int | None - Computation time

    # Usage properties
    msg.cache_read_tokens    # int | None - Cached tokens read
    msg.cache_write_tokens   # int | None - Cached tokens written
    msg.input_tokens         # int | None - Input token count
    msg.output_tokens        # int | None - Output token count

# Example: Find expensive messages
expensive_msgs = [m for m in session.messages if m.cost and m.cost > 0.01]
for msg in expensive_msgs:
    print(f"{msg.role} at {msg.timestamp}: ${msg.cost:.4f}")
```

### Tool Objects

Tool executions are tracked with detailed information:

```python
# ToolExecution - Represents a single tool use
for tool_exec in session.tool_executions:
    tool_exec.tool_name      # str - Name of the tool (e.g., "Bash", "Read")
    tool_exec.input_data     # dict - Tool input parameters
    tool_exec.output         # str | None - Tool output/result
    tool_exec.error          # str | None - Error message if failed
    tool_exec.timestamp      # datetime - When tool was executed
    tool_exec.message_uuid   # str - UUID of containing message

# ToolUseBlock - Part of message content
for msg in session.messages:
    for block in msg.content:
        if isinstance(block, ToolUseBlock):
            block.type           # Literal["tool_use"]
            block.id             # str - Unique block ID
            block.name           # str - Tool name
            block.input          # dict - Tool parameters

# Example: Analyze Bash commands
bash_commands = []
for tool in session.tool_executions:
    if tool.tool_name == "Bash":
        command = tool.input_data.get("command", "")
        bash_commands.append({
            "command": command,
            "output": tool.output,
            "error": tool.error,
            "timestamp": tool.timestamp
        })

print(f"Found {len(bash_commands)} Bash commands")
```

## Common Usage Patterns

### Project Analysis

```python
from claude_sdk import find_projects, load_project

# Find and analyze all projects
projects = find_projects()
for project_path in projects[:5]:
    project = load_project(project_path)
    print(f"{project.name}: {project.total_sessions} sessions, ${project.total_cost:.2f}")
```

### Session Filtering

```python
from claude_sdk import find_sessions, load

# Find sessions for specific project
sessions = find_sessions(project="apply-model")
for session_path in sessions:
    session = load(session_path)
    if session.total_cost > 1.0:  # Expensive sessions
        print(f"{session.session_id}: ${session.total_cost:.2f}")
```

### Tool Analysis

```python
# Analyze tool usage across a project
project = load_project("apply-model")
total_tool_uses = sum(project.tool_usage_count.values())

for tool, count in sorted(project.tool_usage_count.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / total_tool_uses) * 100
    print(f"{tool}: {count} uses ({percentage:.1f}%)")

# Extract specific tool executions
for session in project.sessions:
    for tool in session.tool_executions:
        if tool.tool_name == "Write" and tool.error:
            print(f"Write error in {session.session_id}: {tool.error}")
```

## API Reference

### Core Functions

#### `load(file_path)`
Load a Claude Code session from a JSONL file.
- **Args**: `file_path` - Path to the JSONL session file
- **Returns**: `Session` object
- **Raises**: `ParseError`, `FileNotFoundError`

#### `find_sessions(base_path=None, project=None)`
Find Claude Code session files, optionally filtered by project.
- **Args**:
  - `base_path` - Directory to search (defaults to ~/.claude/projects/)
  - `project` - Project name or path to filter sessions
- **Returns**: List of session file paths
- **Example**:
  ```python
  # Find all sessions
  all_sessions = find_sessions()

  # Find sessions in specific project
  project_sessions = find_sessions(project="apply-model")
  ```

#### `find_projects(base_path=None)`
Find all Claude Code project directories.
- **Args**: `base_path` - Directory to search (defaults to ~/.claude/projects/)
- **Returns**: List of project directory paths

#### `load_project(project_identifier, base_path=None)`
Load a Claude Code project with all its sessions.
- **Args**:
  - `project_identifier` - Project name or full path
  - `base_path` - Base directory (defaults to ~/.claude/projects/)
- **Returns**: `Project` object with aggregated data

## Error Handling

The SDK provides a clean error hierarchy:

```python
from claude_sdk import load, ClaudeSDKError, ParseError

try:
    session = load("conversation.jsonl")
except FileNotFoundError:
    print("Session file not found!")
except ParseError as e:
    print(f"Error parsing session: {e}")
except ClaudeSDKError as e:
    print(f"General SDK error: {e}")
```

## Development

This project uses modern Python tooling:

- **uv** for fast dependency management
- **basedpyright** for strict type checking
- **ruff** for formatting and linting
- **pytest** for testing
- **just** for convenient commands

### Development Commands

```bash
# Install dependencies
just install

# Run all checks
just check

# Format code
just fmt

# Type check
just typecheck

# Run tests
just test

# Run tests with coverage
just test-cov
```

## Performance

The SDK is optimized for large session files:

- Memory-efficient streaming parser for JSONL files
- Single-pass algorithms for metadata calculation
- Efficient conversation threading reconstruction
- Handles sessions with 1000+ messages without excessive memory usage

## License

MIT License - see LICENSE file for details.
