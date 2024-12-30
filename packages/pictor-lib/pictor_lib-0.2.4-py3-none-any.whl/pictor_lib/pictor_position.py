"""Module that defines the PictorPosition class."""
from decimal import Decimal

from src.pictor_lib.pictor_type import DecimalUnion
from src.pictor_lib.pictor_size import PictorSize


class PictorPosition(tuple[Decimal, Decimal]):
    """Wrap 2d position (x, y)."""

    def __new__(cls, x: DecimalUnion = 0, y: DecimalUnion = 0):
        return tuple.__new__(PictorPosition, (Decimal(x), Decimal(y)))

    @property
    def x(self) -> Decimal:
        """The x property."""

        return self[0]

    @property
    def y(self) -> Decimal:
        """The y property."""

        return self[1]

    @property
    def raw_tuple(self) -> tuple[int, int]:
        """Convert to rounded int tuple which can be used in raw Pillow APIs."""

        return round(self[0]), round(self[1])

    def set_x(self, x: DecimalUnion) -> 'PictorPosition':
        """Set the x property and return a new instance."""

        return PictorPosition(x, self[1])

    def set_y(self, y: DecimalUnion) -> 'PictorPosition':
        """Set the y property and return a new instance."""

        return PictorPosition(self[0], y)

    def move(self, offset: PictorSize) -> 'PictorPosition':
        """Return a new instance by moving the given offset."""

        return PictorPosition(self.x + offset.width, self.y + offset.height)

    def move_x(self, offset: DecimalUnion) -> 'PictorPosition':
        """Return a new instance by moving the x field of given offset."""

        return PictorPosition(self.x + offset, self.y)

    def move_y(self, offset: DecimalUnion) -> 'PictorPosition':
        """Return a new instance by moving the y field of given offset."""

        return PictorPosition(self.x, self.y + offset)
