"""Dataclasses for the core module."""

from dataclasses import dataclass

@dataclass
class Cords:
    """A simple dataclass to store x and y coordinates."""
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Cords):
            return Cords(self.x + other.x, self.y + other.y)
        elif isinstance(other, tuple) and len(other) == 2:
            return Cords(self.x + other[0], self.y + other[1])
        raise TypeError(f"Unsupported operand type(s) for +: 'Cords' and '{type(other).__name__}'")

    def __iadd__(self, other):
        if isinstance(other, Cords):
            self.x += other.x
            self.y += other.y
        elif isinstance(other, tuple) and len(other) == 2:
            self.x += other[0]
            self.y += other[1]
        else:
            text = f"Unsupported operand type(s) for +=: 'Cords' and '{type(other).__name__}'"
            raise TypeError(text)
        return self

    def __sub__(self, other):
        if isinstance(other, Cords):
            return Cords(self.x - other.x, self.y - other.y)
        elif isinstance(other, tuple) and len(other) == 2:
            return Cords(self.x - other[0], self.y - other[1])
        raise TypeError(f"Unsupported operand type(s) for -: 'Cords' and '{type(other).__name__}'")

    def __isub__(self, other):
        if isinstance(other, Cords):
            self.x -= other.x
            self.y -= other.y
        elif isinstance(other, tuple) and len(other) == 2:
            self.x -= other[0]
            self.y -= other[1]
        else:
            text = f"Unsupported operand type(s) for -=: 'Cords' and '{type(other).__name__}'"
            raise TypeError(text)
        return self

@dataclass
class Size:
    """A simple dataclass to store width and height."""
    width: int
    height: int
