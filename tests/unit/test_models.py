"""Unit tests for claude_sdk.models foundation types."""

from datetime import datetime
from pathlib import Path
from uuid import UUID

import pytest

from claude_sdk.models import (
    ClaudeSDKBaseModel,
    DateTimeType,
    MessageType,
    PathType,
    Role,
    StopReason,
    UserType,
    UUIDType,
)


class TestUserType:
    """Test UserType enum."""

    def test_enum_values(self):
        """Test UserType has correct string values."""
        assert UserType.EXTERNAL == "external"
        assert UserType.INTERNAL == "internal"

    def test_enum_membership(self):
        """Test UserType membership."""
        assert UserType.EXTERNAL in UserType
        assert UserType.INTERNAL in UserType
        assert "external" in [e.value for e in UserType]
        assert "internal" in [e.value for e in UserType]
        assert "invalid" not in [e.value for e in UserType]

    def test_string_inheritance(self):
        """Test UserType inherits from str."""
        assert isinstance(UserType.EXTERNAL, str)
        assert isinstance(UserType.INTERNAL, str)


class TestMessageType:
    """Test MessageType enum."""

    def test_enum_values(self):
        """Test MessageType has correct string values."""
        assert MessageType.USER == "user"
        assert MessageType.ASSISTANT == "assistant"

    def test_enum_membership(self):
        """Test MessageType membership."""
        assert MessageType.USER in MessageType
        assert MessageType.ASSISTANT in MessageType
        assert "user" in [e.value for e in MessageType]
        assert "assistant" in [e.value for e in MessageType]
        assert "system" not in [e.value for e in MessageType]

    def test_string_inheritance(self):
        """Test MessageType inherits from str."""
        assert isinstance(MessageType.USER, str)
        assert isinstance(MessageType.ASSISTANT, str)


class TestRole:
    """Test Role enum."""

    def test_enum_values(self):
        """Test Role has correct string values."""
        assert Role.USER == "user"
        assert Role.ASSISTANT == "assistant"

    def test_enum_membership(self):
        """Test Role membership."""
        assert Role.USER in Role
        assert Role.ASSISTANT in Role
        assert "user" in [e.value for e in Role]
        assert "assistant" in [e.value for e in Role]
        assert "system" not in [e.value for e in Role]

    def test_string_inheritance(self):
        """Test Role inherits from str."""
        assert isinstance(Role.USER, str)
        assert isinstance(Role.ASSISTANT, str)

    def test_role_message_type_compatibility(self):
        """Test Role and MessageType have compatible values."""
        assert Role.USER.value == MessageType.USER.value
        assert Role.ASSISTANT.value == MessageType.ASSISTANT.value


class TestStopReason:
    """Test StopReason enum."""

    def test_enum_values(self):
        """Test StopReason has correct string values."""
        assert StopReason.END_TURN == "end_turn"
        assert StopReason.MAX_TOKENS == "max_tokens"
        assert StopReason.STOP_SEQUENCE == "stop_sequence"

    def test_enum_membership(self):
        """Test StopReason membership."""
        assert StopReason.END_TURN in StopReason
        assert StopReason.MAX_TOKENS in StopReason
        assert StopReason.STOP_SEQUENCE in StopReason
        assert "end_turn" in [e.value for e in StopReason]
        assert "max_tokens" in [e.value for e in StopReason]
        assert "stop_sequence" in [e.value for e in StopReason]
        assert "timeout" not in [e.value for e in StopReason]

    def test_string_inheritance(self):
        """Test StopReason inherits from str."""
        assert isinstance(StopReason.END_TURN, str)
        assert isinstance(StopReason.MAX_TOKENS, str)
        assert isinstance(StopReason.STOP_SEQUENCE, str)


class TestClaudeSDKBaseModel:
    """Test ClaudeSDKBaseModel configuration."""

    def test_frozen_config(self):
        """Test models are frozen (immutable)."""

        class TestModel(ClaudeSDKBaseModel):
            value: str

        model = TestModel(value="test")

        # Should raise error when trying to modify frozen model
        with pytest.raises(ValueError, match="frozen"):
            model.value = "changed"

    def test_extra_forbid_config(self):
        """Test models forbid extra fields."""

        class TestModel(ClaudeSDKBaseModel):
            value: str

        # Should raise error for unexpected fields
        with pytest.raises(ValueError, match="Extra inputs are not permitted"):
            TestModel(value="test", unexpected_field="invalid")

    def test_model_inheritance(self):
        """Test ClaudeSDKBaseModel inherits from BaseModel."""
        from pydantic import BaseModel

        assert issubclass(ClaudeSDKBaseModel, BaseModel)

    def test_config_dict_settings(self):
        """Test ConfigDict has correct settings."""
        config = ClaudeSDKBaseModel.model_config
        assert config["frozen"] is True
        assert config["extra"] == "forbid"


class TestTypeAliases:
    """Test type aliases for common types."""

    def test_uuid_type_alias(self):
        """Test UUIDType alias."""
        assert UUIDType is UUID
        test_uuid = UUIDType("12345678-1234-5678-9abc-123456789012")
        assert isinstance(test_uuid, UUID)

    def test_datetime_type_alias(self):
        """Test DateTimeType alias."""
        assert DateTimeType is datetime
        test_datetime = DateTimeType.now()
        assert isinstance(test_datetime, datetime)

    def test_path_type_alias(self):
        """Test PathType alias."""
        assert PathType is Path
        test_path = PathType("/test/path")
        assert isinstance(test_path, Path)


class TestEnumJSONCompatibility:
    """Test enums work correctly with JSON serialization."""

    def test_enum_json_values(self):
        """Test all enums use string values compatible with JSON."""
        # All enum values should be strings
        for enum_type in [UserType, MessageType, Role, StopReason]:
            for member in enum_type:
                assert isinstance(member.value, str)
                assert len(member.value) > 0

    def test_enum_serialization(self):
        """Test enums serialize to their string values."""
        assert UserType.EXTERNAL.value == "external"
        assert MessageType.USER.value == "user"
        assert Role.ASSISTANT.value == "assistant"
        assert StopReason.END_TURN.value == "end_turn"


class TestFoundationTypesExports:
    """Test foundation types are properly exported."""

    def test_all_exports(self):
        """Test __all__ contains all foundation types."""
        from claude_sdk.models import __all__

        expected_exports = {
            "UserType",
            "MessageType",
            "Role",
            "StopReason",
            "ClaudeSDKBaseModel",
            "UUIDType",
            "DateTimeType",
            "PathType",
        }

        assert set(__all__) == expected_exports

    def test_import_all_types(self):
        """Test all foundation types can be imported."""
        # This test passes if imports at top of file succeed
        assert UserType is not None
        assert MessageType is not None
        assert Role is not None
        assert StopReason is not None
        assert ClaudeSDKBaseModel is not None
        assert UUIDType is not None
        assert DateTimeType is not None
        assert PathType is not None
