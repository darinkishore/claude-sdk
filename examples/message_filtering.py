"""Message filtering and analysis example.

This example demonstrates how to use the Claude SDK to:
1. Load a session
2. Filter messages by various criteria
3. Analyze conversation patterns
4. Work with sidechains and message threading
"""

from datetime import timedelta
from pathlib import Path

from claude_sdk import find_sessions, load


def analyze_messages(session_path):
    """Analyze message patterns in a Claude Code session."""
    print(f"\nAnalyzing messages in session: {session_path}")
    print("-" * 60)

    # Load the session
    session = load(session_path)

    # Basic message statistics
    print(f"Total messages: {len(session.messages)}")

    # Get main chain vs sidechain
    main_chain = session.get_main_chain()
    sidechains = [msg for msg in session.messages if msg.is_sidechain]

    print(f"Main conversation chain: {len(main_chain)} messages")
    print(f"Sidechains: {len(sidechains)} messages")

    # Messages by role
    user_messages = session.get_messages_by_role("user")
    assistant_messages = session.get_messages_by_role("assistant")

    print("\nMessages by role:")
    print(f"  User messages: {len(user_messages)}")
    print(f"  Assistant messages: {len(assistant_messages)}")

    # Message timing analysis
    if len(session.messages) > 1:
        sorted_msgs = sorted(session.messages, key=lambda m: m.timestamp)
        first_msg = sorted_msgs[0]
        last_msg = sorted_msgs[-1]

        print("\nConversation timing:")
        print(f"  First message: {first_msg.timestamp}")
        print(f"  Last message: {last_msg.timestamp}")

        if session.duration:
            print(f"  Total duration: {session.duration}")

            # Calculate average time between messages
            if len(sorted_msgs) > 1:
                timestamps = [msg.timestamp for msg in sorted_msgs]
                deltas = [(timestamps[i + 1] - timestamps[i]) for i in range(len(timestamps) - 1)]
                avg_delta = sum(deltas, timedelta()) / len(deltas)
                print(f"  Average time between messages: {avg_delta}")

    # Conversation tree analysis
    tree = session.conversation_tree

    print("\nConversation threading:")
    print(f"  Root messages: {len(tree.root_messages)}")

    # Show thread depth
    max_depth = 0

    def get_thread_depth(uuid, depth=0):
        nonlocal max_depth
        max_depth = max(max_depth, depth)

        # Get children if any
        uuid_str = str(uuid)
        if uuid_str in tree.parent_to_children:
            for child in tree.parent_to_children[uuid_str]:
                get_thread_depth(child, depth + 1)

    # Calculate thread depth for each root
    for root in tree.root_messages:
        get_thread_depth(root)

    print(f"  Maximum thread depth: {max_depth}")

    # If there are sidechains, show an example
    if sidechains:
        print("\nSidechain example:")
        sidechain_msg = sidechains[0]

        # Find the parent message to show context
        parent_uuid = sidechain_msg.parent_uuid
        parent_msg = next((msg for msg in session.messages if msg.uuid == parent_uuid), None)

        if parent_msg:
            parent_text = parent_msg.text
            if len(parent_text) > 100:
                parent_text = parent_text[:97] + "..."

            print(f"  Parent: {parent_msg.role}: {parent_text}")

        # Show the sidechain message
        side_text = sidechain_msg.text
        if len(side_text) > 100:
            side_text = side_text[:97] + "..."

        print(f"  Sidechain: {sidechain_msg.role}: {side_text}")


def main():
    """Main function for message filtering example."""
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

    # Try to find a complex session with multiple messages
    complex_sessions = []
    for path in session_files:
        try:
            session = load(path)
            # Look for sessions with multiple messages
            if len(session.messages) > 5:
                complex_sessions.append((path, len(session.messages)))
        except Exception as e:
            print(f"Error loading {path}: {e}")

    if not complex_sessions:
        # If no complex sessions, just use the first one
        if session_files:
            analyze_messages(session_files[0])
        return

    # Sort by message count and analyze the most complex session
    complex_sessions.sort(key=lambda x: x[1], reverse=True)

    print(f"Found {len(complex_sessions)} complex sessions:")
    for i, (path, count) in enumerate(complex_sessions[:3]):
        print(f"{i + 1}. {path.name}: {count} messages")

    # Analyze the session with the most messages
    most_complex_path = complex_sessions[0][0]
    analyze_messages(most_complex_path)


if __name__ == "__main__":
    main()
