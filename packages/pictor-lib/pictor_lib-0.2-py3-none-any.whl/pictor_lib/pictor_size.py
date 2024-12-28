"""Module that defines the PictorSize class."""
from decimal import Decimal

from src.pictor_lib.pictor_type import DecimalUnion


class PictorSize(tuple[Decimal, Decimal]):
    """Wrap 2d size (width x height)."""

    def __new__(cls, width: DecimalUnion = 0, height: DecimalUnion = 0):
        return tuple.__new__(PictorSize, (Decimal(width), Decimal(height)))

    @property
    def width(self) -> Decimal:
        """The width property."""

        return self[0]

    @property
    def height(self) -> Decimal:
        """The height property."""

        return self[1]

    def set_width(self, width: DecimalUnion) -> 'PictorSize':
        """Set the width property and return a new instance."""

        return PictorSize(width, self[1])

    def set_height(self, height: DecimalUnion) -> 'PictorSize':
        """Set the height property and return a new instance."""

        return PictorSize(self[0], height)

    def scale(self, ratio: DecimalUnion) -> 'PictorSize':
        """Return a new size instance by scaling the width and height by given ratio."""

        return PictorSize(self[0] * Decimal(ratio), self[1] * Decimal(ratio))

    def scale_width(self, ratio: DecimalUnion) -> 'PictorSize':
        """Return a new size instance by scaling the width by given ratio."""

        return PictorSize(self[0] * Decimal(ratio), self[1])

    def scale_height(self, ratio: DecimalUnion) -> 'PictorSize':
        """Return a new size instance by scaling the height by given ratio."""

        return PictorSize(self[0], self[1] * Decimal(ratio))

    def shrink_to_square(self) -> 'PictorSize':
        """Return a new size instance by shrinking the longer side to the shorter side."""

        size = min(self[0], self[1])
        return PictorSize(size, size)

    def expand_to_square(self) -> 'PictorSize':
        """Return a new size instance by expanding the shorter side to the longer side."""

        size = max(self[0], self[1])
        return PictorSize(size, size)

    def __add__(self, other: 'PictorSize') -> 'PictorSize':
        """Return a new size instance by adding another size object to the current object."""

        return PictorSize(self[0] + other[0], self[1] + other[1])

    def __sub__(self, other: 'PictorSize') -> 'PictorSize':
        """Return a new size instance by subtracting another size object from the current object."""

        return PictorSize(self[0] - other[0], self[1] - other[1])

    def __mul__(self, ratio: DecimalUnion) -> 'PictorSize':
        """Return a new size instance by scaling the width and height by given ratio."""

        return self.scale(ratio)
