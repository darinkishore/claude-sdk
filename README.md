# Claude SDK

> Typed Python wrapper for Claude Code CLI

A composable, low-level Python library providing rich abstractions over Claude Code's data model and execution capabilities. Designed for building observability systems, pattern recognition, and downstream optimization tools.

## Development Status

**Currently in T0 phase: Data Access Foundation**

This project is in active development. The core data models and parsing infrastructure are being implemented first.

## Core Principles

- **Modern Monolith**: Single package with clean module separation and clear boundaries
- **Data Access First**: Clean, efficient access to Claude Code's data structures
- **Type Safety**: Full typing with Pydantic runtime validation and basedpyright --strict
- **Minimal Abstractions**: Provide data types and parsers, not opinions
- **Sync-First**: Synchronous API for simplicity (async can be added later)
- **Robust Error Handling**: Sealed error hierarchy with rich context

## Implementation Phases

### T0: Data Access Foundation (Current)
- [ ] Claude Code JSONL format parsing with robust error handling
- [ ] Message threading and conversation reconstruction  
- [ ] Tool usage extraction and correlation
- [ ] Performance metrics access (cost, timing, token usage)
- [ ] Raw data structures with zero interpretation
- [ ] Comprehensive type coverage with basedpyright --strict

### T1: Execution Engine (Next)
- [ ] Claude binary integration (`--output-format json`)
- [ ] Session configuration and management
- [ ] Synchronous subprocess execution with timeout handling
- [ ] Rich error context and recovery strategies
- [ ] Command validation and safety checks

### T2: Git Integration (Future)
- [ ] Git state capture (before/after execution)
- [ ] Diff analysis and file change tracking
- [ ] Commit correlation with session outcomes

### T3: MCP Support (Future)
- [ ] MCP server configuration and management
- [ ] Tool permission handling

## Quick Start

```bash
# Clone and enter the project
cd claude-sdk

# Enter development environment (with Nix)
nix develop

# Or set up manually with uv
uv sync --dev

# Run checks
just check

# Run tests
just test
```

## Project Structure

```
claude_sdk/
├── __init__.py              # Public API exports
├── models.py                # Pydantic data models
├── parser.py                # JSONL parsing and session reconstruction  
├── executor.py              # Claude binary execution
├── errors.py                # Sealed error hierarchy
├── utils.py                 # Common utilities
└── py.typed                 # Type marker file
```

## Development

This project uses modern Python tooling:

- **uv** for fast dependency management
- **basedpyright** for strict type checking  
- **ruff** for formatting and linting
- **pytest** for testing
- **pre-commit** for git hooks
- **just** for convenient commands
- **nix** for reproducible development environment

### Available Commands

```bash
just check          # Run all checks (format, lint, type check, test)
just fmt             # Format code with ruff
just lint            # Lint code with ruff  
just typecheck       # Type check with basedpyright
just test            # Run tests
just test-cov        # Run tests with coverage
just clean           # Clean up build artifacts
just build           # Build package
```

## Documentation

See `docs/PYTHON_CLAUDE_CODE_SDK_SPECIFICATION.md` for the complete technical specification.

## Usage Examples

*Examples will be added as the implementation progresses*

## Contributing

This project is currently in early development. Please see the specification for implementation details and planned features.

## License

MIT License - see LICENSE file for details.