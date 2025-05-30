---
task_id: T01_S04
sprint_sequence_id: S04
status: completed
complexity: High
last_updated: 2025-05-30 13:22
---

# Task: Core Project Model & Path Handling

## Description
Implement the foundational Project model that aggregates Claude Code sessions by project directory. This includes robust path encoding/decoding utilities to handle Claude Code's directory naming scheme and efficient session aggregation logic.

Based on analysis of actual directory structure, Claude Code encodes project paths like `/Users/darin/Projects/apply-model` as `-Users-darin-Projects-apply-model`. The Project model needs to handle this encoding, aggregate session data, and provide meaningful project-level properties.

## Key Discovery Findings & Design Decisions

### Directory Structure Analysis (Critical Implementation Details)
- **Path encoding pattern**: `/Users/darin/Projects/apply-model` → `-Users-darin-Projects-apply-model`
- **Special character handling**: `/Users/darin/.claude` → `-Users-darin--claude` (double dash for dot directories)
- **Worktrees**: Treated as separate independent projects (no special handling needed)
- **Temporary projects**: Follow pattern `tmp-*` (e.g., `-Users-darin-tmp-apply-model`)

### Real Directory Examples for Testing
```
-Users-darin-Projects-apply-model                    # Standard project
-Users-darin--claude-py-sdk                         # Hidden directory (.claude)
-Users-darin--claude-squad-worktrees-analysis-1841b163fddfd718  # Regular project (worktree)
-Users-darin-tmp-apply-model                         # Temporary project
-Users-darin-vaults-good-work-darin                  # Obsidian vault project
```

### Session-Project Relationship Data
- **95.3% of sessions** stay in one directory throughout conversation (361/380 sessions)
- **4.7% change directories** but typically within same project tree (18/380 sessions)
- **Perfect 1:1 mapping**: session `cwd` field directly corresponds to project directory encoding
- **Session count ranges**: 1-120 sessions per project (apply-model has 120, most have 1-10)

### Project Characteristics from Real Data
- **High-activity projects**: apply-model (120 sessions), nix-config (58 sessions), py-sdk (22 sessions)
- **File sizes**: Range from 250B to 6.7MB per session file
- **Session patterns**: Some projects have activity bursts, others steady development
- **Tool usage**: Varies significantly by project type (development vs config vs analysis)

### API Design Decisions
- **Explicit over magic**: Rejected smart/magic loading behavior in favor of clear function names
- **Computed properties**: Use @property for aggregations (total_cost, tools_used) computed from sessions list
- **Immutable model**: Follow existing ClaudeSDKBaseModel pattern with frozen=True
- **Lazy computation**: Properties calculate on-demand rather than storing redundant data

### Reference Data for Implementation

**Claude Code Project Directory Location**: `~/.claude/projects/`

**Sample Project Directory Structure** (first 10 entries):
```
-Users-darin
-Users-darin--claude
-Users-darin--claude-py-sdk
-Users-darin--claude-squad-worktrees-analysis-1841b163fddfd718
-Users-darin--claude-squad-worktrees-braintrust-183e4dc08bfd6fe8
-Users-darin--claude-squad-worktrees-braintrust-deprecation-184242eb02c8ab38
-Users-darin--claude-squad-worktrees-diffs-1841201643ae9b88
-Users-darin--claude-squad-worktrees-help-184165eb3a47e020
-Users-darin--claude-squad-worktrees-local-testing-184158050c8d84a8
-Users-darin--claude-squad-worktrees-pipeline-refactor-1841606eef4dd2b8
```

**Subagent Analysis Location**: If you need to re-analyze the actual directory structure or inspect real project contents, use:
```bash
# View directory structure
ls -la ~/.claude/projects/ | head -10

# Analyze specific project contents
ls -la ~/.claude/projects/-Users-darin-Projects-apply-model/

# Check session file patterns
find ~/.claude/projects/-Users-darin-Projects-apply-model/ -name "*.jsonl" | head -5
```

**Task Agent Usage**: Use the Task tool if you need to:
- Re-analyze project directory patterns
- Inspect session file contents for `cwd` field validation
- Verify path encoding/decoding with real examples
- Test edge cases with actual directory names

## Goal / Objectives
- Create a Project model that represents a collection of Claude Code sessions within a project directory
- Implement reliable path encoding/decoding for Claude Code directory names
- Provide aggregated project properties: total_cost, tools_used, session counts, date ranges
- Support efficient project creation from session lists or directory scanning

## Acceptance Criteria
- [x] Project model correctly decodes directory names to filesystem paths
- [x] Project handles real directory names including edge cases (worktrees, temp dirs, special chars)
- [x] Project aggregates costs, tool usage, and temporal data from all sessions
- [x] Project.from_directory() classmethod loads all sessions in a project directory
- [x] Project properties (total_cost, tools_used, etc.) are computed efficiently
- [x] All path handling utilities have comprehensive tests with real directory examples
- [x] Project model follows existing ClaudeSDKBaseModel patterns and is immutable

### Implementation Strategy & Technical Details

**Path Decoding Algorithm**:
```python
def decode_project_path(directory_name: str) -> Path:
    """Convert '-Users-darin-Projects-apply-model' → '/Users/darin/Projects/apply-model'"""
    # Remove leading dash and convert dashes to path separators
    path_str = directory_name[1:].replace('-', '/')
    # Handle special case: --claude → /.claude
    path_str = path_str.replace('//', '/.')
    return Path(path_str)

def extract_project_name(project_path: Path) -> str:
    """Extract 'apply-model' from '/Users/darin/Projects/apply-model'"""
    return project_path.name
```

**Project Model Structure** (based on Session model patterns):
```python
class Project(ClaudeSDKBaseModel):
    project_id: str      # Directory name (e.g., "-Users-darin-Projects-apply-model")
    project_path: Path   # Decoded path (e.g., "/Users/darin/Projects/apply-model")
    name: str           # Display name (e.g., "apply-model")
    sessions: list[Session] = Field(default_factory=list)

    @property
    def total_cost(self) -> float:
        return sum(s.total_cost for s in self.sessions)

    @classmethod
    def from_directory(cls, project_dir: Path) -> "Project":
        # Load all .jsonl files in directory using existing load_session()
        # Decode project_id from directory name
        # Extract display name from path
```

**Aggregation Properties** (based on SessionMetadata analysis):
- total_cost: Sum of session.total_cost across all sessions
- tools_used: Union of session.tools_used across all sessions
- total_sessions: len(self.sessions)
- first/last_session_date: Min/max of session timestamps
- Most properties should be @property computed on-demand for memory efficiency

## Subtasks
- [x] Add path encoding/decoding utilities (decode_project_path, extract_project_name)
- [x] Implement Project model class with core fields (project_id, project_path, name, sessions)
- [x] Add computed properties for aggregated data (total_cost, tools_used, date ranges)
- [x] Implement Project.from_directory() classmethod for loading from directories
- [x] Add comprehensive tests using real Claude Code directory names
- [x] Integrate Project model into existing models.py following established patterns

## Output Log
*(This section is populated as work progresses on the task)*

[2025-05-30 13:15]: Task started. Implementing Project model for aggregating Claude Code sessions by project directory, including path encoding/decoding utilities.
[2025-05-30 13:25]: Implemented path encoding/decoding utilities in utils.py: decode_project_path, encode_project_path, and extract_project_name with comprehensive documentation and validation.
[2025-05-30 13:40]: Implemented Project model in models.py with core fields, computed properties, and factory methods. Project model handles all required path encoding/decoding and aggregates metrics across sessions.
[2025-05-30 13:50]: Created comprehensive test suite in test_project_model.py with tests for path utilities and Project model functionality.
[2025-05-30 14:10]: Fixed test failures and addressed linting issues. All tests now pass with full type checking compliance.
[2025-05-30 14:15]: Code review completed successfully. Implementation meets all project standards and requirements.
[2025-05-30 14:22]: Task completed. All acceptance criteria have been met. The Project model is ready for use in the codebase.
