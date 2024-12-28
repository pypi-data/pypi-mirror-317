"""Module that defines the PictorPosition class."""
from decimal import Decimal


class PictorPosition(tuple[Decimal, Decimal]):
    """Wrap 2d position (x, y)."""

    def __new__(cls,
                x: int | float | Decimal = 0,
                y: int | float | Decimal = 0):
        return tuple.__new__(PictorPosition, (Decimal(x), Decimal(y)))

    @property
    def x(self) -> Decimal:
        """The x property."""

        return self[0]

    @property
    def y(self) -> Decimal:
        """The y property."""

        return self[1]
