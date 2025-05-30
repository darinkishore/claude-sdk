"""Tool usage analysis example.

This example demonstrates how to use the Claude SDK to:
1. Load a session
2. Analyze tool usage patterns
3. Calculate tool costs
4. Extract detailed tool execution information
"""

from collections import Counter
from pathlib import Path

from claude_sdk import find_sessions, load


def analyze_tool_usage(session_path):
    """Analyze tool usage in a Claude Code session."""
    print(f"\nAnalyzing tool usage in session: {session_path}")
    print("-" * 60)

    # Load the session
    session = load(session_path)

    # Skip if no tools used
    if not session.tools_used:
        print("No tools were used in this session.")
        return

    # Basic tool usage statistics
    print(f"Total tools used: {len(session.tools_used)}")
    print(f"Tool types: {', '.join(sorted(session.tools_used))}")

    # Count tool usage by type
    tool_counts = Counter()
    for msg in session.messages:
        for tool in msg.tools:
            tool_counts[tool] += 1

    print("\nTool usage by type:")
    for tool, count in tool_counts.most_common():
        print(f"  {tool}: {count} uses")

    # Cost analysis if costs are available
    if session.tool_costs:
        print("\nTool costs:")
        total_tool_cost = sum(session.tool_costs.values())
        for tool, cost in sorted(session.tool_costs.items(), key=lambda x: x[1], reverse=True):
            percentage = (cost / total_tool_cost * 100) if total_tool_cost else 0
            print(f"  {tool}: ${cost:.4f} ({percentage:.1f}%)")

    # Detailed tool execution analysis
    if session.tool_executions:
        print(f"\nDetailed tool executions: {len(session.tool_executions)}")

        # Show a sample of tool executions
        max_samples = min(3, len(session.tool_executions))
        print(f"\nSample of {max_samples} tool executions:")

        for i, execution in enumerate(session.tool_executions[:max_samples]):
            print(f"\nExecution {i + 1}:")
            print(f"  Tool: {execution.tool_name}")
            print(f"  Duration: {execution.duration}")
            print(f"  Input: {execution.input}")

            # For most tool executions, show a preview of the output
            if hasattr(execution.output, "content"):
                content = execution.output.content
                if content and len(content) > 100:
                    content = content[:97] + "..."
                print(f"  Output: {content}")

            print(f"  Error: {execution.output.is_error}")


def main():
    """Main function for tool analysis example."""
    # Try to find session files
    try:
        # First look in fixtures for test data
        fixtures_dir = Path(__file__).parent.parent / "tests" / "fixtures"
        session_files = find_sessions(fixtures_dir)

        if not session_files:
            # If no fixtures, look in default location
            print("No session files found in fixtures, checking ~/.claude/projects/")
            session_files = find_sessions()
    except Exception as e:
        print(f"Error finding session files: {e}")
        return

    if not session_files:
        print("No Claude Code session files found.")
        return

    # Find a session with tool usage
    tool_sessions = []
    for path in session_files:
        try:
            session = load(path)
            if session.tools_used:
                tool_sessions.append((path, len(session.tool_executions)))
        except Exception as e:
            print(f"Error loading {path}: {e}")

    if not tool_sessions:
        print("No sessions with tool usage found.")
        return

    # Sort by tool usage count and analyze the session with most tools
    tool_sessions.sort(key=lambda x: x[1], reverse=True)

    print(f"Found {len(tool_sessions)} sessions with tool usage:")
    for i, (path, count) in enumerate(tool_sessions):
        print(f"{i + 1}. {path.name}: {count} tool executions")

    # Analyze the session with the most tool usage
    most_tools_path = tool_sessions[0][0]
    analyze_tool_usage(most_tools_path)


if __name__ == "__main__":
    main()
