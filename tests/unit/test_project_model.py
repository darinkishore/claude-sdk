"""Test suite for Project model and path encoding/decoding utilities."""

from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

from claude_sdk.models import ParsedSession, Project, SessionMetadata
from claude_sdk.utils import decode_project_path, encode_project_path, extract_project_name


class TestPathUtilities:
    """Test suite for project path encoding and decoding utilities."""

    def test_decode_project_path_standard(self):
        """Test standard path decoding."""
        input_path = "-Users-darin-Projects-apply-model"
        expected = Path("/Users/darin/Projects/apply-model")

        result = decode_project_path(input_path)
        assert result == expected

    def test_decode_project_path_hidden_dir(self):
        """Test decoding with hidden directories (double dash)."""
        input_path = "-Users-darin--claude-py-sdk"
        expected = Path("/Users/darin/.claude/py-sdk")

        result = decode_project_path(input_path)
        assert result == expected

    def test_decode_project_path_worktree(self):
        """Test decoding with git worktree paths."""
        input_path = "-Users-darin--claude-squad-worktrees-analysis-1841b163fddfd718"
        expected = Path("/Users/darin/.claude/squad-worktrees/analysis-1841b163fddfd718")

        result = decode_project_path(input_path)
        assert result == expected

    def test_decode_project_path_validation(self):
        """Test validation of invalid paths."""
        # Empty string
        with pytest.raises(ValueError):
            decode_project_path("")

        # No leading dash
        with pytest.raises(ValueError):
            decode_project_path("Users-darin-Projects")

    def test_encode_project_path_standard(self):
        """Test standard path encoding."""
        input_path = Path("/Users/darin/Projects/apply-model")
        expected = "-Users-darin-Projects-apply-model"

        result = encode_project_path(input_path)
        assert result == expected

    def test_encode_project_path_hidden_dir(self):
        """Test encoding with hidden directories."""
        input_path = Path("/Users/darin/.claude/py-sdk")
        expected = "-Users-darin--claude-py-sdk"

        result = encode_project_path(input_path)
        assert result == expected

    def test_encode_project_path_no_leading_slash(self):
        """Test encoding with path that doesn't start with slash."""
        input_path = Path("Users/darin/Projects/apply-model")
        expected = "-Users-darin-Projects-apply-model"

        result = encode_project_path(input_path)
        assert result == expected

    def test_encode_project_path_validation(self):
        """Test validation of invalid paths."""
        # Empty path
        with pytest.raises(ValueError):
            encode_project_path(Path())

    def test_extract_project_name(self):
        """Test project name extraction."""
        test_cases = [
            (Path("/Users/darin/Projects/apply-model"), "apply-model"),
            (Path("/Users/darin/.claude/py-sdk"), "py-sdk"),
            (Path("/tmp/temporary-project"), "temporary-project"),
        ]

        for input_path, expected in test_cases:
            result = extract_project_name(input_path)
            assert result == expected

    def test_extract_project_name_validation(self):
        """Test validation of invalid paths for name extraction."""
        with pytest.raises(ValueError):
            extract_project_name(Path())


class TestProjectModel:
    """Test suite for Project model."""

    def test_project_creation(self):
        """Test basic Project instantiation."""
        project = Project(
            project_id="-Users-darin-Projects-apply-model",
            project_path=Path("/Users/darin/Projects/apply-model"),
            name="apply-model",
        )

        assert project.project_id == "-Users-darin-Projects-apply-model"
        assert project.project_path == Path("/Users/darin/Projects/apply-model")
        assert project.name == "apply-model"
        assert project.sessions == []

    def test_project_validation(self):
        """Test Project model validation."""
        # Missing required fields
        with pytest.raises(ValidationError):
            Project(project_id="-Users-darin-Projects-apply-model")

        with pytest.raises(ValidationError):
            Project(
                project_id="-Users-darin-Projects-apply-model",
                project_path=Path("/Users/darin/Projects/apply-model"),
            )

    def test_project_from_encoded_id(self):
        """Test Project.from_encoded_id factory method."""
        project_id = "-Users-darin-Projects-apply-model"
        project = Project.from_encoded_id(project_id)

        assert project.project_id == project_id
        assert project.project_path == Path("/Users/darin/Projects/apply-model")
        assert project.name == "apply-model"
        assert project.sessions == []

    @patch("claude_sdk.models.encode_project_path")
    def test_project_from_directory(self, mock_encode):
        """Test Project.from_directory factory method."""
        project_dir = Path("/Users/darin/Projects/apply-model")
        mock_encode.return_value = "-Users-darin-Projects-apply-model"

        # Mock directory existence checks
        with (
            patch.object(Path, "exists", return_value=True),
            patch.object(Path, "is_dir", return_value=True),
        ):
            project = Project.from_directory(project_dir)

            assert project.project_id == "-Users-darin-Projects-apply-model"
            assert project.project_path == project_dir
            assert project.name == "apply-model"
            assert project.sessions == []

    def test_project_from_directory_validation(self):
        """Test validation in Project.from_directory factory method."""
        non_existent_dir = Path("/path/does/not/exist")

        # Test with non-existent directory
        with (
            patch.object(Path, "exists", return_value=False),
            pytest.raises(ValueError, match="does not exist"),
        ):
            Project.from_directory(non_existent_dir)

        # Test with file instead of directory
        with (
            patch.object(Path, "exists", return_value=True),
            patch.object(Path, "is_dir", return_value=False),
            pytest.raises(ValueError, match="Not a directory"),
        ):
            Project.from_directory(non_existent_dir)

    def test_property_total_cost(self):
        """Test total_cost property aggregation."""
        # Create mock sessions with costs
        sessions = []
        for cost in [1.25, 0.75, 3.0]:
            mock_session = MagicMock(spec=ParsedSession)
            mock_session.metadata = MagicMock(spec=SessionMetadata)
            mock_session.metadata.total_cost = cost
            sessions.append(mock_session)

        # Create project with mock sessions
        project = Project(
            project_id="-Users-darin-Projects-apply-model",
            project_path=Path("/Users/darin/Projects/apply-model"),
            name="apply-model",
            sessions=sessions,
        )

        assert project.total_cost == 5.0  # 1.25 + 0.75 + 3.0

    def test_property_tools_used(self):
        """Test tools_used property aggregation."""
        # Create mock sessions with tool usage
        sessions = []

        # Session 1: Used Bash, Read
        session1 = MagicMock(spec=ParsedSession)
        session1.metadata = MagicMock(spec=SessionMetadata)
        session1.metadata.tool_usage_count = {"Bash": 2, "Read": 1}
        sessions.append(session1)

        # Session 2: Used Read, Write, Grep
        session2 = MagicMock(spec=ParsedSession)
        session2.metadata = MagicMock(spec=SessionMetadata)
        session2.metadata.tool_usage_count = {"Read": 3, "Write": 1, "Grep": 2}
        sessions.append(session2)

        # Create project with mock sessions
        project = Project(
            project_id="-Users-darin-Projects-apply-model",
            project_path=Path("/Users/darin/Projects/apply-model"),
            name="apply-model",
            sessions=sessions,
        )

        assert project.tools_used == {"Bash", "Read", "Write", "Grep"}

    def test_property_total_sessions(self):
        """Test total_sessions property."""
        # Create mock sessions
        sessions = [MagicMock(spec=ParsedSession) for _ in range(3)]

        # Create project with mock sessions
        project = Project(
            project_id="-Users-darin-Projects-apply-model",
            project_path=Path("/Users/darin/Projects/apply-model"),
            name="apply-model",
            sessions=sessions,
        )

        assert project.total_sessions == 3

    def test_property_session_dates(self):
        """Test first_session_date and last_session_date properties."""
        # Create mock sessions with timestamps
        sessions = []
        dates = [
            datetime(2025, 5, 1, 10, 0),
            datetime(2025, 5, 10, 14, 30),
            datetime(2025, 4, 15, 9, 45),
        ]

        for date in dates:
            mock_session = MagicMock(spec=ParsedSession)
            mock_session.metadata = MagicMock(spec=SessionMetadata)
            mock_session.metadata.session_start = date
            mock_session.metadata.session_end = date + timedelta(hours=1)
            sessions.append(mock_session)

        # Create project with mock sessions
        project = Project(
            project_id="-Users-darin-Projects-apply-model",
            project_path=Path("/Users/darin/Projects/apply-model"),
            name="apply-model",
            sessions=sessions,
        )

        assert project.first_session_date == datetime(2025, 4, 15, 9, 45)  # Earliest date
        assert project.last_session_date == datetime(2025, 5, 10, 15, 30)  # Latest end date

    def test_property_total_duration(self):
        """Test total_duration property."""
        # Create mock sessions with timestamps
        sessions = []
        start_date = datetime(2025, 4, 15, 9, 45)
        end_date = datetime(2025, 5, 10, 15, 30)

        # First session (earliest)
        mock_session1 = MagicMock(spec=ParsedSession)
        mock_session1.metadata = MagicMock(spec=SessionMetadata)
        mock_session1.metadata.session_start = start_date
        mock_session1.metadata.session_end = start_date + timedelta(hours=1)
        sessions.append(mock_session1)

        # Second session (latest)
        mock_session2 = MagicMock(spec=ParsedSession)
        mock_session2.metadata = MagicMock(spec=SessionMetadata)
        mock_session2.metadata.session_start = end_date - timedelta(hours=1)
        mock_session2.metadata.session_end = end_date
        sessions.append(mock_session2)

        # Create project with mock sessions
        project = Project(
            project_id="-Users-darin-Projects-apply-model",
            project_path=Path("/Users/darin/Projects/apply-model"),
            name="apply-model",
            sessions=sessions,
        )

        # Expected: Time from earliest session start to latest session end
        expected_duration = end_date - start_date
        assert project.total_duration == expected_duration

    def test_property_tool_usage_count(self):
        """Test tool_usage_count property aggregation."""
        # Create mock sessions with tool usage
        sessions = []

        # Session 1: Used Bash (2), Read (1)
        session1 = MagicMock(spec=ParsedSession)
        session1.metadata = MagicMock(spec=SessionMetadata)
        session1.metadata.tool_usage_count = {"Bash": 2, "Read": 1}
        sessions.append(session1)

        # Session 2: Used Read (3), Write (1), Grep (2)
        session2 = MagicMock(spec=ParsedSession)
        session2.metadata = MagicMock(spec=SessionMetadata)
        session2.metadata.tool_usage_count = {"Read": 3, "Write": 1, "Grep": 2}
        sessions.append(session2)

        # Create project with mock sessions
        project = Project(
            project_id="-Users-darin-Projects-apply-model",
            project_path=Path("/Users/darin/Projects/apply-model"),
            name="apply-model",
            sessions=sessions,
        )

        expected_counts = {
            "Bash": 2,
            "Read": 4,  # 1 + 3
            "Write": 1,
            "Grep": 2,
        }

        assert project.tool_usage_count == expected_counts
