"""Test module for the class PictorSize."""

from decimal import Decimal
import pytest
from assertpy import assert_that

from src.pictor_lib.pictor_size import PictorSize


class TestPictorSize:
    """Tests for the class PictorSize."""

    def test_new_with_defaults(self):
        """Test for creating a new object with defaults."""

        size = PictorSize()

        # Verify size.
        assert_that(size.width).is_equal_to(0)
        assert_that(size.height).is_equal_to(0)

    def test_new_with_values(self):
        """Test for creating a new object with values."""

        size = PictorSize(width=800, height=600)

        # Verify size.
        assert_that(size.width).is_equal_to(800)
        assert_that(size.height).is_equal_to(600)

    def test_setters(self):
        """Test for creating a new object with values."""

        old_size = PictorSize(width=67, height=42)
        new_size = old_size.set_width(800).set_height(600)

        # Verify size.
        assert_that(new_size).is_not_same_as(old_size)
        assert_that(new_size.width).is_equal_to(800)
        assert_that(new_size.height).is_equal_to(600)

    @pytest.mark.parametrize("ratio", [0.0, 1.0, 2.0, 0.5])
    def test_scale(self, ratio: float):
        """Test for the scale method."""

        old_size = PictorSize(800, 600)
        new_size = old_size.scale(ratio)

        # Verify size.
        assert_that(new_size).is_not_same_as(old_size)
        assert_that(new_size.width).is_equal_to(old_size.width *
                                                Decimal(ratio))
        assert_that(new_size.height).is_equal_to(old_size.height *
                                                 Decimal(ratio))

    @pytest.mark.parametrize("ratio", [0.0, 1.0, 2.0, 0.5])
    def test_scale_width(self, ratio: float):
        """Test for the scale_width method."""

        old_size = PictorSize(800, 600)
        new_size = old_size.scale_width(ratio)

        # Verify size.
        assert_that(new_size).is_not_same_as(old_size)
        assert_that(new_size.width).is_equal_to(old_size.width *
                                                Decimal(ratio))
        assert_that(new_size.height).is_equal_to(old_size.height)

    @pytest.mark.parametrize("ratio", [0.0, 1.0, 2.0, 0.5])
    def test_scale_height(self, ratio: float):
        """Test for the scale_height method."""

        old_size = PictorSize(800, 600)
        new_size = old_size.scale_height(ratio)

        # Verify size.
        assert_that(new_size).is_not_same_as(old_size)
        assert_that(new_size.width).is_equal_to(old_size.width)
        assert_that(new_size.height).is_equal_to(old_size.height *
                                                 Decimal(ratio))

    def test_shrink_to_square_when_for_longer_width(self):
        """Test for the shrink_to_square method for longer width."""

        old_size = PictorSize(800, 600)
        new_size = old_size.shrink_to_square()

        # Verify size.
        assert_that(new_size).is_not_same_as(old_size)
        assert_that(new_size.width).is_equal_to(600)
        assert_that(new_size.height).is_equal_to(600)

    def test_shrink_to_square_when_for_longer_height(self):
        """Test for the shrink_to_square method for longer height."""

        old_size = PictorSize(600, 800)
        new_size = old_size.shrink_to_square()

        # Verify size.
        assert_that(new_size).is_not_same_as(old_size)
        assert_that(new_size.width).is_equal_to(600)
        assert_that(new_size.height).is_equal_to(600)

    def test_shrink_to_square_when_for_square(self):
        """Test for the shrink_to_square method for equal width and height."""

        old_size = PictorSize(600, 600)
        new_size = old_size.shrink_to_square()

        # Verify size.
        assert_that(new_size).is_not_same_as(old_size)
        assert_that(new_size.width).is_equal_to(600)
        assert_that(new_size.height).is_equal_to(600)

    def test_expand_to_square_when_for_longer_width(self):
        """Test for the expand_to_square method for longer width."""

        old_size = PictorSize(800, 600)
        new_size = old_size.expand_to_square()

        # Verify size.
        assert_that(new_size).is_not_same_as(old_size)
        assert_that(new_size.width).is_equal_to(800)
        assert_that(new_size.height).is_equal_to(800)

    def test_expand_to_square_when_for_longer_height(self):
        """Test for the expand_to_square method for longer height."""

        old_size = PictorSize(600, 800)
        new_size = old_size.expand_to_square()

        # Verify size.
        assert_that(new_size).is_not_same_as(old_size)
        assert_that(new_size.width).is_equal_to(800)
        assert_that(new_size.height).is_equal_to(800)

    def test_expand_to_square_when_for_square(self):
        """Test for the expand_to_square method for equal width and height."""

        old_size = PictorSize(800, 800)
        new_size = old_size.expand_to_square()

        # Verify size.
        assert_that(new_size).is_not_same_as(old_size)
        assert_that(new_size.width).is_equal_to(800)
        assert_that(new_size.height).is_equal_to(800)

    def test_add_operator(self):
        """Test for the __add__ operator."""

        size_1 = PictorSize(800, 600)
        size_2 = PictorSize(67, 42)
        new_size = size_1 + size_2

        # Verify size.
        assert_that(size_1).is_equal_to(PictorSize(800, 600))
        assert_that(size_2).is_equal_to(PictorSize(67, 42))
        assert_that(new_size).is_not_same_as(size_1)
        assert_that(new_size).is_not_same_as(size_2)
        assert_that(new_size.width).is_equal_to(867)
        assert_that(new_size.height).is_equal_to(642)

    def test_sub_operator(self):
        """Test for the __sub__ operator."""

        size_1 = PictorSize(800, 600)
        size_2 = PictorSize(67, 42)
        new_size = size_2 - size_1

        # Verify size.
        assert_that(size_1).is_equal_to(PictorSize(800, 600))
        assert_that(size_2).is_equal_to(PictorSize(67, 42))
        assert_that(new_size).is_not_same_as(size_1)
        assert_that(new_size).is_not_same_as(size_2)
        assert_that(new_size.width).is_equal_to(-733)
        assert_that(new_size.height).is_equal_to(-558)

    @pytest.mark.parametrize("ratio", [0.0, 1.0, 2.0, 0.5])
    def test_mul_operator(self, ratio: float):
        """Test for the __mul__ operator."""

        old_size = PictorSize(800, 600)
        new_size = old_size * ratio

        # Verify size.
        assert_that(new_size).is_not_same_as(old_size)
        assert_that(new_size.width).is_equal_to(old_size.width *
                                                Decimal(ratio))
        assert_that(new_size.height).is_equal_to(old_size.height *
                                                 Decimal(ratio))
