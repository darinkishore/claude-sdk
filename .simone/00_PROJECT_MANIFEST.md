---
project_name: Python Claude Code SDK
current_milestone_id: M01
highest_sprint_in_milestone: S04
current_sprint_id: S01
status: active
last_updated: 2025-05-29 16:13
---

# Project Manifest: Python Claude Code SDK

This manifest serves as the central reference point for the project. It tracks the current focus and links to key documentation.

## 1. Project Vision & Overview

A simple Python library for parsing Claude Code session files (JSONL) and extracting structured data. Focus: **read existing sessions, get the data out cleanly**.

The SDK provides clean, efficient access to Claude Code's JSONL data with Pydantic models for all data structures and a simple API: `parse_session(file_path)` → structured data.

This project follows a milestone-based development approach.

## 2. Current Focus

- **Milestone:** M01 - Core Session Parser
- **Sprint:** S01 - Data Models & Type System Foundation (in progress - T01_S01 ✅ completed, T02_S01 ✅ completed, T03_S01 🔄 in progress)

## 3. Milestones Overview

### M01: Core Session Parser (🎯 CURRENT)
**Goal**: Parse Claude Code JSONL files → clean Python objects

**Sprint Roadmap**:

#### S01: Data Models & Type System Foundation (🔄 IN PROGRESS - T01_S01)
- Complete Pydantic data model layer
- MessageRecord, ParsedSession, content blocks, enums
- Full basedpyright compliance and type safety

#### S02: JSONL Parser & Error Handling (📋 PLANNED)
- Raw JSONL parsing with robust error handling
- Memory-efficient processing for large files
- Session file discovery utilities

#### S03: Session Reconstruction & Metadata Aggregation (📋 PLANNED)
- Conversation threading via parent_uuid relationships
- Session metadata calculation (costs, tokens, tool usage)
- ParsedSession container with complete session data

#### S04: Public API & Library Integration (📋 PLANNED)
- parse_session() and discover_sessions() functions
- Clean public interface and documentation
- Production-ready library distribution

### M02: Analysis Helpers (📋 PLANNED)
**Goal**: Make the parsed data actually useful

**What we add**:
- Session discovery: `discover_sessions()`
- Tool usage analysis
- Cost/token aggregation
- Export utilities (JSON, CSV)

## 4. Key Documentation

- [Architecture Documentation](./01_PROJECT_DOCS/ARCHITECTURE.md)
- [Current Milestone Requirements](./02_REQUIREMENTS/M01_Core_Session_Parser/)
- [General Tasks](./04_GENERAL_TASKS/)

## 5. Quick Links

- **Current Task:** T03_S01_Message_Record_Model (implementing MessageRecord model with complete JSONL field mapping)
- **Current Sprint:** [S01 Data Models](./03_SPRINTS/S01_M01_Data_Models/)
- **Current Requirements:** [M01 Core Session Parser PRD](./02_REQUIREMENTS/M01_Core_Session_Parser/PRD_Core_Session_Parser.md)
- **Project Reviews:** [Latest Review](./10_STATE_OF_PROJECT/)

## 6. Development Status

**S01 Sprint Progress** - T01_S01_Foundation_Types completed ✅. T02_S01_Content_Block_Models completed ✅ (content block types: TextBlock, ThinkingBlock, ToolUseBlock). T03_S01_Message_Record_Model in progress 🔄 (implementing core MessageRecord model with JSONL mapping).

**Estimated Timeline**: 4 weeks (1 week per sprint) to complete M01 Core Session Parser milestone. S01 started 2025-05-29.
