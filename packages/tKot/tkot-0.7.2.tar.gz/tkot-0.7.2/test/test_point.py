import unittest
from copy import copy
from tKot.common import Point, Polygon, Box


class TestType(unittest.TestCase):

    def test_init(self):
        point = Point(0, 0)
        self.assertEqual(point.x, 0, "compare x")

    def test_reduce(self):
        point = Point(10, 10)
        point2 = Point(100, 100) - point
        self.assertEqual(point2, Point(90, 90))

    def test_add(self):
        point = Point(10, 10)
        point2 = Point(100, 100) + point
        self.assertEqual(point2, Point(110, 110))

    def test_unpack(self):
        point = Point(10, 10)
        self.assertEqual(list(point), [10, 10])

    def test_floordiv(self):
        point = Point(10, 10)
        self.assertEqual(point // 2, Point(5, 5))

    def test_idiv(self):
        point = Point(10, 10)
        p_div = Point(2, 3)
        res = point / p_div
        self.assertEqual(point // 2, Point(5, 5))

    def test_copy(self):
        p = Point(10, 10)
        p2 = copy(p)
        print(id(p2), id(p))

    def test_Polygon(self):
        pol = Polygon(4, 0, 24, 0, 24, 4, 13, 4, 13, 9, 10, 9, 10, 33, 27, 33, 27, 9, 13, 9,
                      13, 4, 24, 4, 24, 0, 33, 0, 37, 4, 37, 38, 33, 42, 4, 42, 0, 38, 0, 4)
        pol = pol.reshape(Point(100, 100))
        point = Point(3, 5)
        pol *= Point(2, 1)
        pol += point
        print(*pol)

    def test_Box(self):
        box = Box(0, 0, 10, 10)
