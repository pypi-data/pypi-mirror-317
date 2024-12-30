"""Test module for the class PictorPoint."""

from decimal import Decimal
import pytest
from assertpy import assert_that

from src.pictor_lib.pictor_point import PictorPoint
from src.pictor_lib.pictor_size import PictorSize


# pylint: disable=too-many-public-methods
class TestPictorPoint:
    """Tests for the class PictorPoint."""

    def test_origin(self):
        """Test for origin point."""

        point = PictorPoint.ORIGIN

        # Verify point.
        assert_that(point.x).is_equal_to(0)
        assert_that(point.y).is_equal_to(0)
        assert_that(point.raw_tuple).is_equal_to((0, 0))

    def test_new_with_values(self):
        """Test for creating a new object with values."""

        point = PictorPoint(x=67, y=42)

        # Verify point.
        assert_that(point.x).is_equal_to(67)
        assert_that(point.y).is_equal_to(42)
        assert_that(point.raw_tuple).is_equal_to((67, 42))

    def test_new_with_decimal_values(self):
        """Test for creating a new object with decimal values."""

        point = PictorPoint(x=Decimal(3.14159), y=Decimal(2.71828))

        # Verify point.
        assert_that(point.x).is_equal_to(Decimal(3.14159))
        assert_that(point.y).is_equal_to(Decimal(2.71828))
        assert_that(point.raw_tuple).is_equal_to((3, 3))

    def test_setters(self):
        """Test for creating a new object with values."""

        old_point = PictorPoint(x=67, y=42)
        new_point = old_point.set_x(800).set_y(600)

        # Verify point.
        assert_that(new_point).is_not_same_as(old_point)
        assert_that(new_point.x).is_equal_to(800)
        assert_that(new_point.y).is_equal_to(600)

    @pytest.mark.parametrize("t", [(0, 0), (67, 31), (67, -31), (-67, 31), (-67, -31)])
    def test_move(self, t: tuple[int,int]):
        """Test for the move method."""

        offset = PictorSize(t[0], t[1])
        old_point = PictorPoint(x=42, y=13)
        new_point = old_point.move(offset)

        # Verify point.
        assert_that(new_point).is_not_same_as(old_point)
        assert_that(new_point.x).is_equal_to(42 + t[0])
        assert_that(new_point.y).is_equal_to(13 + t[1])

    @pytest.mark.parametrize("offset", [0, 42, -42])
    def test_move_x(self, offset: Decimal):
        """Test for the move_x method."""

        old_point = PictorPoint(x=13, y=42)
        new_point = old_point.move_x(offset)

        # Verify point.
        assert_that(new_point).is_not_same_as(old_point)
        assert_that(new_point.x).is_equal_to(13 + offset)
        assert_that(new_point.y).is_equal_to(42)

    @pytest.mark.parametrize("offset", [0, 42, -42])
    def test_move_y(self, offset: Decimal):
        """Test for the move_y method."""

        old_point = PictorPoint(x=42, y=13)
        new_point = old_point.move_y(offset)

        # Verify point.
        assert_that(new_point).is_not_same_as(old_point)
        assert_that(new_point.x).is_equal_to(42)
        assert_that(new_point.y).is_equal_to(13 + offset)
