#!/usr/bin/env python3
"""
Script to check if Claude Code sessions change working directories (cwd) during a conversation.
Analyzes actual session files from ~/.claude/projects/ to understand cwd behavior.
"""

import json
import sys
from collections import defaultdict
from pathlib import Path


def analyze_session_file(session_path: Path) -> tuple[str, set[str], int]:
    """Analyze a single session file for cwd changes.

    Returns:
        (session_id, unique_cwds, total_messages)
    """
    unique_cwds = set()
    session_id = None
    message_count = 0

    try:
        with Path(session_path).open() as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue

                try:
                    record = json.loads(line)
                    message_count += 1

                    if session_id is None:
                        session_id = record.get("sessionId", "unknown")

                    cwd = record.get("cwd")
                    if cwd:
                        unique_cwds.add(cwd)

                except json.JSONDecodeError as e:
                    print(f"JSON error in {session_path}:{line_num}: {e}")
                    continue

    except Exception as e:
        print(f"Error reading {session_path}: {e}")
        return "error", set(), 0

    return session_id or "unknown", unique_cwds, message_count


def main():
    """Analyze all Claude Code session files for cwd behavior."""
    claude_projects_dir = Path.home() / ".claude" / "projects"

    if not claude_projects_dir.exists():
        print(f"Claude projects directory not found: {claude_projects_dir}")
        sys.exit(1)

    print(f"Analyzing Claude Code sessions in: {claude_projects_dir}")
    print("=" * 80)

    # Statistics
    total_sessions = 0
    sessions_with_cwd_changes = 0
    project_stats = defaultdict(lambda: {"sessions": 0, "sessions_with_changes": 0})
    all_cwd_changes = []

    # Analyze each project directory
    for project_dir in sorted(claude_projects_dir.iterdir()):
        if not project_dir.is_dir():
            continue

        project_name = project_dir.name
        session_files = list(project_dir.glob("*.jsonl"))

        if not session_files:
            continue

        print(f"\nProject: {project_name}")
        print(f"  Session files: {len(session_files)}")

        project_stats[project_name]["sessions"] = len(session_files)

        for session_file in session_files:
            total_sessions += 1
            session_id, unique_cwds, message_count = analyze_session_file(session_file)

            if len(unique_cwds) > 1:
                sessions_with_cwd_changes += 1
                project_stats[project_name]["sessions_with_changes"] += 1
                all_cwd_changes.append((project_name, session_file.name, session_id, unique_cwds))

                print(f"    📁 {session_file.name}: {len(unique_cwds)} different cwds")
                for cwd in sorted(unique_cwds):
                    print(f"        {cwd}")
            else:
                print(f"    ✅ {session_file.name}: 1 cwd ({message_count} messages)")

    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total sessions analyzed: {total_sessions}")
    print(f"Sessions with cwd changes: {sessions_with_cwd_changes}")
    print(f"Percentage with changes: {sessions_with_cwd_changes / total_sessions * 100:.1f}%")

    if all_cwd_changes:
        print("\nDETAILS OF SESSIONS WITH CWD CHANGES:")
        print("-" * 40)
        for project, session_file, session_id, cwds in all_cwd_changes:
            print(f"\nProject: {project}")
            print(f"Session: {session_file} (ID: {session_id})")
            print(f"Working directories ({len(cwds)}):")
            for cwd in sorted(cwds):
                print(f"  - {cwd}")

    # Project breakdown
    print("\nPROJECT BREAKDOWN:")
    print("-" * 40)
    for project, stats in sorted(project_stats.items()):
        change_pct = (
            (stats["sessions_with_changes"] / stats["sessions"] * 100)
            if stats["sessions"] > 0
            else 0
        )
        print(
            f"{project}: {stats['sessions_with_changes']}/{stats['sessions']} sessions with changes ({change_pct:.1f}%)"
        )


if __name__ == "__main__":
    main()
