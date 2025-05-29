---
task_id: T03_S01
sprint_sequence_id: S01
status: open
complexity: High
last_updated: 2025-05-29T14:06:01Z
---

# Task: MessageRecord Model

## Description
Implement the core MessageRecord Pydantic model that directly maps to Claude Code JSONL line structure. This is the central data structure that represents individual session records.

## Goal / Objectives
Create a comprehensive MessageRecord model that accurately represents JSONL data:
- Complete mapping of all JSONL fields to Pydantic model fields
- Proper handling of nested Message and TokenUsage structures
- Support for field aliases matching JSONL naming conventions
- Robust validation of UUID fields and datetime parsing
- Full compatibility with real Claude Code session data

## Acceptance Criteria
- [ ] MessageRecord model with all required fields from JSONL structure
- [ ] Nested Message model with role, content list, stop_reason, usage
- [ ] TokenUsage model for input/output/cache token tracking
- [ ] Proper field aliases for snake_case to camelCase mapping
- [ ] UUID validation for parent_uuid and uuid fields
- [ ] Datetime parsing and validation for timestamp field
- [ ] Path validation for cwd field
- [ ] Optional field handling for cost_usd, duration_ms, request_id
- [ ] Unit tests with real JSONL data examples
- [ ] Full basedpyright compliance

## Subtasks
- [ ] Create TokenUsage model with all token count fields
- [ ] Create Message model with role, content, stop_reason, usage
- [ ] Implement MessageRecord with all JSONL fields
- [ ] Configure field aliases (parentUuid, isSidechain, userType, etc.)
- [ ] Add UUID validation for parent_uuid and uuid fields
- [ ] Add datetime validation and parsing for timestamp
- [ ] Add Path validation for cwd field
- [ ] Configure optional fields with proper default handling
- [ ] Implement proper content field as List[ContentBlock] union
- [ ] Create comprehensive unit tests with JSONL examples
- [ ] Validate model can parse real session file records

## Implementation Guidance
Reference the detailed model structure in `docs/PYTHON_CLAUDE_CODE_SDK_SPECIFICATION.md` lines 183-221 for complete field mapping. Critical points:
- Use Field(alias="...") for camelCase JSONL field names
- parent_uuid should be Optional[UUID] with None default
- cost_usd and duration_ms are optional performance metrics
- content field uses discriminated union of content blocks
- Proper validation is essential for parsing real session data

## Related Documentation
- [Technical Specification](../../../docs/PYTHON_CLAUDE_CODE_SDK_SPECIFICATION.md) - Complete MessageRecord definition
- [PRD Core Session Parser](../../02_REQUIREMENTS/M01_Core_Session_Parser/PRD_Core_Session_Parser.md) - MessageRecord requirements (FR-2.1)

## Dependencies
- T01_S01_Foundation_Types must be completed (requires enums)
- T02_S01_Content_Block_Models must be completed (requires content blocks)

## Output Log
*(This section is populated as work progresses on the task)*
