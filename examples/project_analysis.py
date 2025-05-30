"""
Project analysis example for Claude Code SDK.

This example demonstrates using the Project API to analyze multiple sessions across projects.
It shows:
1. Finding and loading projects
2. Accessing project-level aggregated data
3. Filtering sessions by project
4. Creating project-level reports

Usage:
    python project_analysis.py
"""

from claude_sdk import find_projects, find_sessions, load, load_project


def list_projects():
    """Find and list all available projects."""
    print("=== Available Projects ===")

    try:
        # Find all projects
        projects = find_projects()

        if not projects:
            print("No projects found in ~/.claude/projects/")
            return []

        print(f"Found {len(projects)} projects\n")

        # Print project information
        for i, project_path in enumerate(projects[:10]):  # Show first 10 projects
            # Extract project name from path for display
            project_name = project_path.name
            print(f"{i + 1}. {project_name}")

        if len(projects) > 10:
            print(f"...and {len(projects) - 10} more")

        return projects

    except Exception as e:
        print(f"Error finding projects: {e}")
        return []


def analyze_project(project_path):
    """Analyze a specific project in detail."""
    print(f"\n=== Analyzing Project: {project_path.name} ===")

    try:
        # Load the project
        project = load_project(project_path)

        # Basic project info
        print(f"Project name: {project.name}")
        print(f"Project path: {project.project_path}")
        print(f"Total sessions: {project.total_sessions}")
        print(f"Total cost: ${project.total_cost:.4f}")

        # Time span
        if project.first_session_date and project.last_session_date:
            first_date = project.first_session_date.strftime("%Y-%m-%d %H:%M")
            last_date = project.last_session_date.strftime("%Y-%m-%d %H:%M")
            print(f"First session: {first_date}")
            print(f"Last session: {last_date}")

            if project.total_duration:
                days = project.total_duration.days
                hours = project.total_duration.seconds // 3600
                print(f"Project duration: {days} days, {hours} hours")

        # Tool usage
        print("\nTool Usage:")
        for tool, count in sorted(
            project.tool_usage_count.items(), key=lambda x: x[1], reverse=True
        ):
            print(f"  {tool}: {count} uses")

        # Sessions
        print("\nTop 5 sessions by cost:")
        for i, session in enumerate(
            sorted(project.sessions, key=lambda s: s.metadata.total_cost, reverse=True)[:5]
        ):
            date = (
                session.metadata.session_start.strftime("%Y-%m-%d %H:%M")
                if session.metadata.session_start
                else "Unknown"
            )
            print(
                f"  {i + 1}. {date} - ${session.metadata.total_cost:.4f} ({len(session.messages)} messages)"
            )

    except Exception as e:
        print(f"Error analyzing project: {e}")


def compare_projects(project_paths, limit=3):
    """Compare multiple projects side by side."""
    if len(project_paths) < 2:
        print("Need at least 2 projects to compare")
        return

    print("\n=== Project Comparison ===")

    try:
        # Load all projects
        projects = []
        for path in project_paths[:limit]:
            try:
                project = load_project(path)
                projects.append(project)
            except Exception as e:
                print(f"Error loading project {path.name}: {e}")

        if len(projects) < 2:
            print("Not enough projects loaded to compare")
            return

        # Print comparison table header
        header = "Metric".ljust(25)
        for project in projects:
            header += project.name.ljust(20)
        print(header)
        print("-" * (25 + 20 * len(projects)))

        # Compare basic metrics
        metrics = {
            "Total sessions": [p.total_sessions for p in projects],
            "Total cost ($)": [f"{p.total_cost:.2f}" for p in projects],
            "Tools used": [len(p.tools_used) for p in projects],
            "First session": [
                p.first_session_date.strftime("%Y-%m-%d") if p.first_session_date else "Unknown"
                for p in projects
            ],
            "Last session": [
                p.last_session_date.strftime("%Y-%m-%d") if p.last_session_date else "Unknown"
                for p in projects
            ],
        }

        for metric, values in metrics.items():
            row = metric.ljust(25)
            for value in values:
                row += str(value).ljust(20)
            print(row)

        # Compare tool usage
        print("\nTop tools by project:")
        for _i, project in enumerate(projects):
            print(f"\n{project.name}:")
            for tool, count in sorted(
                project.tool_usage_count.items(), key=lambda x: x[1], reverse=True
            )[:3]:
                print(f"  {tool}: {count} uses")

    except Exception as e:
        print(f"Error comparing projects: {e}")


def find_sessions_by_project(project_name):
    """Find all sessions for a specific project by name."""
    print(f"\n=== Finding Sessions for Project: {project_name} ===")

    try:
        # Find sessions filtered by project
        sessions = find_sessions(project=project_name)

        if not sessions:
            print(f"No sessions found for project '{project_name}'")
            return

        print(f"Found {len(sessions)} sessions")

        # Print session information
        for i, session_path in enumerate(sessions[:5]):  # Show first 5 sessions
            # Load session to get details
            try:
                session = load(session_path)
                date = (
                    session.metadata.session_start.strftime("%Y-%m-%d %H:%M")
                    if session.metadata.session_start
                    else "Unknown"
                )
                print(
                    f"{i + 1}. {date} - ${session.metadata.total_cost:.4f} ({len(session.messages)} messages)"
                )
            except Exception as e:
                print(f"{i + 1}. {session_path.name} - Error: {e}")

        if len(sessions) > 5:
            print(f"...and {len(sessions) - 5} more")

    except Exception as e:
        print(f"Error finding sessions: {e}")


def main():
    """Main function demonstrating project analysis capabilities."""
    # List all available projects
    projects = list_projects()

    if not projects:
        print("No projects found to analyze")
        return

    # Analyze the most recent project
    if projects:
        analyze_project(projects[0])

    # Compare multiple projects
    if len(projects) >= 3:
        compare_projects(projects[:3])

    # Find sessions for a specific project
    if projects:
        # Extract project name from first project
        project_name = projects[0].name
        find_sessions_by_project(project_name)


if __name__ == "__main__":
    main()
