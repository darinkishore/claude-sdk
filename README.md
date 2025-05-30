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
pip install claude-sdk
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

## Project-Level Analysis

The SDK now supports project-level analysis, allowing you to aggregate data across all sessions in a Claude Code project:

```python
from claude_sdk import find_projects, load_project

# Discover all projects
projects = find_projects()
print(f"Found {len(projects)} projects")

# List project names
for i, project_path in enumerate(projects[:5]):
    print(f"{i+1}. {project_path.name}")

# Load a project by name or path
project = load_project("apply-model")  # By name
# OR
project = load_project(projects[0])  # By path

# Access aggregated project data
print(f"Project: {project.name}")
print(f"Total sessions: {project.total_sessions}")
print(f"Total cost: ${project.total_cost:.4f}")
print(f"Tools used: {', '.join(project.tools_used)}")

# Tool usage breakdown
for tool, count in project.tool_usage_count.items():
    print(f"{tool}: {count} uses")

# Access individual sessions
for session in project.sessions[:5]:
    print(f"Session {session.session_id}: ${session.total_cost:.4f}")
```

## Key Concepts

### Session Object

The `Session` class is your primary interface to Claude Code session data:

```python
session = load("conversation.jsonl")

# Core properties
session.session_id          # Unique session identifier
session.messages            # List of Message objects
session.total_cost          # Total session cost in USD
session.tools_used          # Set of tool names used
session.duration            # Session duration as timedelta

# Analysis properties
session.tool_costs          # Cost breakdown by tool
session.cost_by_turn        # Cost per message turn
session.tool_executions     # Detailed tool execution records
```

### Message Object

Each message in a session provides rich information:

```python
for msg in session.messages:
    msg.role                # "user" or "assistant"
    msg.text                # Full message text content
    msg.cost                # Message cost if available
    msg.is_sidechain        # True if in a sidechain
    msg.timestamp           # Message creation time
    msg.uuid                # Unique message identifier
    msg.parent_uuid         # Parent message UUID
    msg.tools               # List of tools used
```

### Project Object

The `Project` class aggregates data across all sessions in a Claude Code project:

```python
project = load_project("apply-model")

# Core properties
project.name                # Human-readable project name
project.project_path        # Full path to project directory
project.sessions            # List of all sessions in the project
project.total_sessions      # Number of sessions

# Aggregated data
project.total_cost          # Total cost across all sessions
project.tools_used          # Set of all tools used
project.tool_usage_count    # Dict mapping tools to usage counts
project.first_session_date  # Earliest session start time
project.last_session_date   # Latest session start time
project.total_duration      # Time span from first to last session
```

## Tool Usage Analysis

Analyze tool patterns and costs:

```python
from claude_sdk import load

session = load("conversation.jsonl")

# Get cost breakdown by tool
for tool, cost in session.tool_costs.items():
    print(f"{tool}: ${cost:.4f} USD")

# Analyze Bash tool usage
bash_commands = []
for msg in session.messages:
    if "Bash" in msg.tools:
        bash_commands.append(msg.text)

print(f"Found {len(bash_commands)} Bash commands")
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
