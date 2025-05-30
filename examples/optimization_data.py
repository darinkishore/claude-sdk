"""Example showing how to extract data for external optimization tools.

This example demonstrates how to use the Claude SDK to:
1. Extract structured data from Claude Code sessions
2. Prepare datasets for external analysis
3. Export cost and usage metrics for optimization
4. Identify patterns that could lead to cost savings
"""

import csv
import json
from datetime import datetime
from pathlib import Path

from claude_sdk import find_sessions, load


def extract_optimization_data(output_dir=None):
    """Extract optimization data from Claude Code sessions.

    Args:
        output_dir: Directory to save output files (defaults to current directory)
    """
    # Set output directory
    if output_dir is None:
        output_dir = Path.cwd()
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(exist_ok=True, parents=True)

    # Find sessions
    print("Finding Claude Code sessions...")
    session_paths = find_sessions()

    if not session_paths:
        print("No Claude Code sessions found.")
        return

    print(f"Found {len(session_paths)} sessions.")
    print("Extracting optimization data...")

    # Initialize data collections
    message_costs = []  # For message-level cost analysis
    tool_usage = []  # For tool usage patterns
    session_summary = []  # For session-level metrics

    # Process each session
    for path in session_paths[:10]:  # Limit to 10 sessions for the example
        try:
            session = load(path)
            session_id = session.session_id

            # Extract session-level data
            session_summary.append(
                {
                    "session_id": session_id,
                    "timestamp": session.messages[0].timestamp.isoformat()
                    if session.messages
                    else None,
                    "total_cost": session.total_cost,
                    "message_count": len(session.messages),
                    "tool_count": len(session.tools_used),
                    "duration_seconds": session.duration.total_seconds()
                    if session.duration
                    else None,
                    "tools_used": ",".join(session.tools_used),
                }
            )

            # Extract message-level data
            for msg in session.messages:
                message_costs.append(
                    {
                        "session_id": session_id,
                        "message_uuid": str(msg.uuid),
                        "timestamp": msg.timestamp.isoformat() if msg.timestamp else None,
                        "role": msg.role,
                        "cost": msg.cost or 0.0,
                        "is_sidechain": msg.is_sidechain,
                        "text_length": len(msg.text),
                        "tool_count": len(msg.tools),
                    }
                )

            # Extract tool usage data
            for msg in session.messages:
                for tool_name in msg.tools:
                    # Find the actual tool blocks for details
                    tool_blocks = msg.get_tool_blocks()
                    for block in tool_blocks:
                        if block.name == tool_name:
                            # Extract tool-specific data
                            tool_usage.append(
                                {
                                    "session_id": session_id,
                                    "message_uuid": str(msg.uuid),
                                    "timestamp": msg.timestamp.isoformat()
                                    if msg.timestamp
                                    else None,
                                    "tool_name": tool_name,
                                    "input_size": len(str(block.input)) if block.input else 0,
                                    "output_size": len(str(block.output)) if block.output else 0,
                                    "is_error": getattr(block.output, "is_error", False),
                                }
                            )

            print(f"Processed session: {session_id} (${session.total_cost:.4f})")

        except Exception as e:
            print(f"Error processing {path.name}: {e}")

    # Skip export if no data was collected
    if not session_summary:
        print("No data was collected.")
        return

    # Export data to CSV files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Export session summary
    session_csv_path = output_dir / f"session_summary_{timestamp}.csv"
    with session_csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=session_summary[0].keys())
        writer.writeheader()
        writer.writerows(session_summary)

    # Export message costs
    if message_costs:
        message_csv_path = output_dir / f"message_costs_{timestamp}.csv"
        with message_csv_path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=message_costs[0].keys())
            writer.writeheader()
            writer.writerows(message_costs)

    # Export tool usage
    if tool_usage:
        tool_csv_path = output_dir / f"tool_usage_{timestamp}.csv"
        with tool_csv_path.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=tool_usage[0].keys())
            writer.writeheader()
            writer.writerows(tool_usage)

    # Create combined JSON for data science tools
    json_path = output_dir / f"claude_optimization_data_{timestamp}.json"
    with json_path.open("w") as f:
        json.dump(
            {"sessions": session_summary, "messages": message_costs, "tool_usage": tool_usage},
            f,
            indent=2,
        )

    print("\nOptimization data extraction complete!")
    print(f"Processed {len(session_summary)} sessions")
    print(f"Extracted data for {len(message_costs)} messages")
    print(f"Analyzed {len(tool_usage)} tool usages")
    print("\nOutput files:")
    print(f"- Session summary: {session_csv_path}")
    if message_costs:
        print(f"- Message costs: {message_csv_path}")
    if tool_usage:
        print(f"- Tool usage: {tool_csv_path}")
    print(f"- Combined JSON: {json_path}")

    print("\nNext steps:")
    print("1. Import these CSV files into your data analysis tool of choice")
    print("2. Look for patterns in tool usage and costs")
    print("3. Identify optimization opportunities by analyzing:")
    print("   - Messages with high costs")
    print("   - Tools with frequent errors")
    print("   - Sessions with long durations")


def main():
    """Main function for optimization data extraction example."""
    extract_optimization_data()


if __name__ == "__main__":
    main()
