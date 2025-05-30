---
task_id: T02_S04
sprint_sequence_id: S04
status: open
complexity: Medium
last_updated: 2025-05-30 12:54
---

# Task: Enhanced Discovery & Loading API

## Description
Implement the enhanced discovery and loading functions that enable project-based workflows. This includes find_projects(), load_project(), enhanced find_sessions() with project filtering, and session-to-project back-references.

The API should follow the established patterns from the existing codebase while adding project-level functionality. Functions should be explicit and non-magical, supporting both project names ("apply-model") and full paths for flexibility.

## Key Discovery Findings & Design Decisions

### API Design Process Results
- **Rejected Approach 1** (Workspace-centric): Too heavy for simple cases
- **Rejected Approach 2** (Separate modules): Created mental model split
- **Rejected Approach 3** (Smart unified load): Magic behavior unacceptable
- **✅ Chose Approach 4** (Clean explicit functions): Maps to actual use cases, no magic

### Function Signatures & Behavior Specifications
```python
# Project discovery
def find_projects(base_path: Path | None = None) -> list[Path]:
    """Find project directories (not session files). Returns directory paths."""

# Project loading
def load_project(project_identifier: str | Path) -> Project:
    """Load by name ('apply-model') or full path ('/path/to/project')"""

# Enhanced session discovery
def find_sessions(base_path: Path | None = None, project: str | None = None) -> list[Path]:
    """Find sessions, optionally filtered by project name"""
```

### Session-to-Project Relationship Details
- **Session.project_path**: Extract from first message's `cwd` field (95.3% consistent)
- **Session.project_name**: Extract display name from project_path
- **Edge case**: Sessions that change `cwd` - use first message's `cwd` as canonical project
- **Worktrees**: Treated as separate independent projects (no special handling needed)
- **Implementation**: Add @property methods to Session class, don't store redundant data

### Real Usage Patterns from Analysis
```python
# Primary discovery workflow
projects = find_projects()                    # Get all project directories
project = load_project("apply-model")        # Load specific project by name

# Session filtering workflow
all_sessions = find_sessions()               # All sessions across all projects
project_sessions = find_sessions(project="apply-model")  # Filtered to one project

# Navigation between levels
project.sessions[0].project_name             # Navigate from session back to project
```

## Goal / Objectives
- Provide project discovery with find_projects() function
- Enable project loading with load_project() supporting both names and paths
- Enhance find_sessions() with optional project filtering
- Add session-to-project navigation properties
- Update public API exports to include new functions

## Acceptance Criteria
- [ ] find_projects() discovers all project directories in ~/.claude/projects/
- [ ] load_project() loads project by name ("apply-model") or full path
- [ ] find_sessions(project="name") filters sessions to specific project
- [ ] Session objects have .project_name and .project_path properties
- [ ] All discovery functions handle errors gracefully with informative messages
- [ ] Public API (__init__.py) exports new functions with proper documentation
- [ ] New functions follow existing parser.py patterns and error handling

### Implementation Strategy & Technical Details

**Existing Code Patterns to Follow**:
- **Error handling**: Use ParseError for user-facing errors (see parser.py:32-48)
- **Discovery pattern**: Follow discover_sessions() structure (base_path defaulting, recursive search)
- **Loading pattern**: Follow parse_complete_session() → Session.from_parsed_session() flow
- **Public API pattern**: Update __init__.py following existing exports and docstring style

**Project Name Resolution Logic**:
```python
def resolve_project_path(project_identifier: str | Path, base_path: Path) -> Path:
    """Resolve 'apply-model' → '/path/to/-Users-darin-Projects-apply-model' directory"""
    if isinstance(project_identifier, Path):
        return project_identifier  # Full path provided

    # Name provided - search for matching directory
    for project_dir in base_path.iterdir():
        decoded_path = decode_project_path(project_dir.name)
        if decoded_path.name == project_identifier:
            return project_dir

    raise ParseError(f"Project '{project_identifier}' not found")
```

**Session Filtering Implementation**:
```python
def find_sessions(base_path: Path | None = None, project: str | None = None) -> list[Path]:
    if project is None:
        return discover_sessions(base_path)  # Existing behavior

    # Filter to specific project directory
    project_dir = resolve_project_path(project, base_path or default_projects_path)
    return list(project_dir.glob("*.jsonl"))
```

**Session Property Addition** (in session.py):
```python
@property
def project_path(self) -> Path:
    """Get project filesystem path from session cwd."""
    if not self.messages:
        raise ValueError("Cannot determine project path from empty session")
    return Path(self.messages[0].cwd)

@property
def project_name(self) -> str:
    """Get project display name from session cwd."""
    return self.project_path.name
```

**Public API Integration** (update __init__.py):
```python
# Add to imports
from .parser import find_projects, load_project

# Add to __all__
__all__ = [
    # Existing exports...
    "find_projects",
    "load_project",
    # Rename for consistency
    "load_session",  # was "load"
]
```

**Error Handling Requirements**:
- Project not found: Clear ParseError with suggestion to run find_projects()
- Empty project directory: ParseError explaining no sessions found
- Invalid project directory: ParseError with path validation message
- Session loading failures: Propagate existing ParseError from load_session()

### Reference Data for Implementation

**Claude Code Project Directory Location**: `~/.claude/projects/`

**Testing Commands**: If you need to validate implementation with real data:
```bash
# List available projects
ls ~/.claude/projects/ | head -10

# Check specific project structure
ls -la ~/.claude/projects/-Users-darin-Projects-apply-model/

# Verify session files exist
find ~/.claude/projects/ -name "*.jsonl" | head -5

# Test project name resolution
echo "-Users-darin-Projects-apply-model" | # should resolve to "apply-model"
```

**Task Agent Usage**: Use the Task tool to:
- Test find_projects() with real directory data
- Validate load_project() name resolution logic
- Test find_sessions(project="name") filtering
- Verify session.project_name/.project_path properties

## Subtasks
- [ ] Implement find_projects() function in parser.py
- [ ] Implement load_project() function supporting name and path resolution
- [ ] Update find_sessions() to accept optional project parameter
- [ ] Add session-to-project properties to Session class
- [ ] Update __init__.py exports and documentation
- [ ] Add integration tests for project-based workflows
- [ ] Update examples to demonstrate project-level usage

## Output Log
*(This section is populated as work progresses on the task)*
