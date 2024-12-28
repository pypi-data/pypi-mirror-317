from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self
from itertools import cycle, batched


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

    def __truediv__(self, other: Self):
        return self.__class__(
            self.x / other.x,
            self.y / other.y
        )

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


class Coords(ABC):
    _coords: tuple[int, ...]

    def __init__(self, *coords: int):
        self._coords = coords
        self.validate()

    @abstractmethod
    def validate(self):
        """runtime init check"""

    def __add__(self, other: Point):
        if isinstance(other, Point):
            it_ = cycle(other.to_tuple())
            return self.__class__(*(coord + next(it_) for coord in self._coords))
        else:
            raise TypeError(F"for add of {self.__class__.__name__}")

    def __mul__(self, other: int | float | Point):
        if isinstance(other, (int, float)):
            return self.__class__(*(int(coord * other) for coord in self._coords))
        elif isinstance(other, Point):
            return self.__class__(*(int(coord * (other.y if i % 2 else other.x)) for i, coord in enumerate(self._coords)))
        else:
            raise TypeError(F"for multiplicate of {self.__class__.__name__}")

    def __iter__(self):
        return iter(self._coords)


class Polygon(Coords):
    def validate(self):
        if len(self._coords) % 2 != 0:
            raise ValueError(F"{self.__class__.__name__} got not pair values")

    @property
    def size(self) -> Point:
        """area occupied by polygon"""
        x_ = list()
        y_ = list()
        for x, y in batched(self._coords, 2):
            x_.append(x)
            y_.append(y)
        return Point(max(x_) - min(x_), max(y_) - min(y_))

    @property
    def base(self) -> Point:
        """upper left point"""
        x_ = list()
        y_ = list()
        for x, y in batched(self._coords, 2):
            x_.append(x)
            y_.append(y)
        return Point(min(x_), min(y_))

    def move_to(self, p: Point) -> Self:
        """move base to Point<x, y>"""
        return self + (p - self.base)

    def reshape(self, shape: Point) -> Self:
        return self * (shape / self.size)


class Box(Polygon):
    def validate(self):
        if len(self._coords) != 4:
            raise ValueError(F"got coords[{len(self._coords)}], expected 4")
