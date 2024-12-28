"""Test module for the class PictorPosition."""

from src.pictor_lib.pictor_position import PictorPosition


class TestPictorPosition:
    """Tests for the class PictorPosition."""

    def test_new_position_with_defaults(self):
        """Test for creating a new object with defaults."""

        position = PictorPosition()

        # Verify position.
        assert position.x == 0
        assert position.y == 0

    def test_new_position_with_values(self):
        """Test for creating a new object with values."""

        position = PictorPosition(x=67, y=42)

        # Verify position.
        assert position.x == 67
        assert position.y == 42
