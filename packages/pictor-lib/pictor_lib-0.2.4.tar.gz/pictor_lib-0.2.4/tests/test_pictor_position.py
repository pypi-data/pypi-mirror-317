"""Test module for the class PictorPosition."""

from decimal import Decimal
import pytest
from assertpy import assert_that

from src.pictor_lib.pictor_position import PictorPosition
from src.pictor_lib.pictor_size import PictorSize


# pylint: disable=too-many-public-methods
class TestPictorPosition:
    """Tests for the class PictorPosition."""

    def test_new_with_defaults(self):
        """Test for creating a new object with defaults."""

        position = PictorPosition()

        # Verify position.
        assert_that(position.x).is_equal_to(0)
        assert_that(position.y).is_equal_to(0)
        assert_that(position.raw_tuple).is_equal_to((0, 0))

    def test_new_with_values(self):
        """Test for creating a new object with values."""

        position = PictorPosition(x=67, y=42)

        # Verify position.
        assert_that(position.x).is_equal_to(67)
        assert_that(position.y).is_equal_to(42)
        assert_that(position.raw_tuple).is_equal_to((67, 42))

    def test_new_with_decimal_values(self):
        """Test for creating a new object with decimal values."""

        position = PictorPosition(x=Decimal(3.14159), y=Decimal(2.71828))

        # Verify position.
        assert_that(position.x).is_equal_to(Decimal(3.14159))
        assert_that(position.y).is_equal_to(Decimal(2.71828))
        assert_that(position.raw_tuple).is_equal_to((3, 3))

    def test_setters(self):
        """Test for creating a new object with values."""

        old_position = PictorPosition(x=67, y=42)
        new_position = old_position.set_x(800).set_y(600)

        # Verify position.
        assert_that(new_position).is_not_same_as(old_position)
        assert_that(new_position.x).is_equal_to(800)
        assert_that(new_position.y).is_equal_to(600)

    @pytest.mark.parametrize("t", [(0, 0), (67, 31), (67, -31), (-67, 31), (-67, -31)])
    def test_move(self, t: tuple[int,int]):
        """Test for the move method."""

        offset = PictorSize(t[0], t[1])
        old_position = PictorPosition(x=42, y=13)
        new_position = old_position.move(offset)

        # Verify position.
        assert_that(new_position).is_not_same_as(old_position)
        assert_that(new_position.x).is_equal_to(42 + t[0])
        assert_that(new_position.y).is_equal_to(13 + t[1])

    @pytest.mark.parametrize("offset", [0, 42, -42])
    def test_move_x(self, offset: Decimal):
        """Test for the move_x method."""

        old_position = PictorPosition(x=13, y=42)
        new_position = old_position.move_x(offset)

        # Verify position.
        assert_that(new_position).is_not_same_as(old_position)
        assert_that(new_position.x).is_equal_to(13 + offset)
        assert_that(new_position.y).is_equal_to(42)

    @pytest.mark.parametrize("offset", [0, 42, -42])
    def test_move_y(self, offset: Decimal):
        """Test for the move_y method."""

        old_position = PictorPosition(x=42, y=13)
        new_position = old_position.move_y(offset)

        # Verify position.
        assert_that(new_position).is_not_same_as(old_position)
        assert_that(new_position.x).is_equal_to(42)
        assert_that(new_position.y).is_equal_to(13 + offset)
