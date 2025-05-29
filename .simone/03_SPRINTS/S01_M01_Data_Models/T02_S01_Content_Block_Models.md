---
task_id: T02_S01
sprint_sequence_id: S01
status: open
complexity: Medium
last_updated: 2025-05-29T14:06:01Z
---

# Task: Content Block Models

## Description
Implement Pydantic models for all content block types that appear in Claude Code JSONL messages. These models represent the different types of content within user and assistant messages.

## Goal / Objectives
Create type-safe content block models that accurately represent message content:
- Implement all content block types: TextBlock, ThinkingBlock, ToolUseBlock
- Ensure proper inheritance from ContentBlock base class
- Handle type discrimination for Union types in message content
- Enable accurate parsing of real JSONL content data

## Acceptance Criteria
- [ ] ContentBlock base class with type discriminator field
- [ ] TextBlock model for plain text content
- [ ] ThinkingBlock model for reasoning content with signature
- [ ] ToolUseBlock model for tool invocations with input parameters
- [ ] Proper Pydantic discriminated union configuration
- [ ] All models validate against real JSONL content examples
- [ ] Full basedpyright compliance
- [ ] Unit tests for each content block type

## Subtasks
- [ ] Implement ContentBlock base class with type field
- [ ] Create TextBlock model with text field
- [ ] Create ThinkingBlock model with thinking and signature fields
- [ ] Create ToolUseBlock model with id, name, and input fields
- [ ] Configure Pydantic discriminated union for ContentBlock types
- [ ] Add proper field validation for tool input (Dict[str, Any])
- [ ] Implement comprehensive docstrings
- [ ] Create unit tests with realistic content block data
- [ ] Test discriminated union parsing works correctly

## Implementation Guidance
Reference the detailed model definitions in `docs/PYTHON_CLAUDE_CODE_SDK_SPECIFICATION.md` lines 160-182 for exact field types and structure. Key considerations:
- Use Literal type annotations for type discriminator
- Tool input should be Dict[str, Any] to handle arbitrary JSON
- Thinking signature field stores reasoning metadata
- All content blocks should be frozen=True for immutability

## Related Documentation
- [Technical Specification](../../../docs/PYTHON_CLAUDE_CODE_SDK_SPECIFICATION.md) - Complete model definitions
- [PRD Core Session Parser](../../02_REQUIREMENTS/M01_Core_Session_Parser/PRD_Core_Session_Parser.md) - Content block requirements (FR-2.2)

## Dependencies
- T01_S01_Foundation_Types must be completed (requires base model class)

## Output Log
*(This section is populated as work progresses on the task)*