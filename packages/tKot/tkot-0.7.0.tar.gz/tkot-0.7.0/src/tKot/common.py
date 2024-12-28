from dataclasses import dataclass
from typing import Self
from itertools import cycle


@dataclass
class Point:
    x: int = 0
    y: int = 0

    @property
    def decoding(self):
        return self.x, self.y

    def move(self, value: int):
        self.x += value
        self.y += value

    def __str__(self):
        return F'<{self.x},{self.y}>'

    def __mul__(self, other: int | float) -> Self:
        """:return Point with scaler x and y by other value"""
        if isinstance(other, (int, float)):
            return Point(int(self.x*other), int(self.y*other))
        else:
            ValueError(F"got unsupport type: {other}, expected int or float")

    def __sub__(self, other: Self) -> Self:
        return self.__class__(
            self.x - other.x,
            self.y - other.y)

    def __add__(self, other) -> Self:
        return self.__class__(
            self.x + other.x,
            self.y + other.y)

    def __floordiv__(self, other: int):
        return self.__class__(
            self.x // other,
            self.y // other)

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        else:
            raise StopIteration

    def to_tuple(self) -> tuple[int, int]:
        return self.x, self.y

    #
    # def __iter__(self):
    #     return iter((self.x, self.y))


class Polygon:
    __coords: tuple[int, ...]

    def __init__(self, *coords: int):
        self.__coords = coords
        if len(self.__coords) % 2 != 0:
            raise ValueError(F"{self.__class__.__name__} got not pair values")

    def __add__(self, other: Point):
        if isinstance(other, Point):
            it_ = cycle(other.to_tuple())
            return self.__class__(*(coord + next(it_) for coord in self.__coords))
        else:
            raise TypeError(F"for add of {self.__class__.__name__}")

    def __mul__(self, other: int | float):
        if isinstance(other, (int, float)):
            return self.__class__(*(int(coord * other) for coord in self.__coords))
        else:
            raise TypeError(F"for multiplicate of {self.__class__.__name__}")


@dataclass
class Box:
    x1: int
    y1: int
    x2: int
    y2: int

    def __iter__(self):
        return iter((self.x1, self.y1, self.x2, self.y2))
