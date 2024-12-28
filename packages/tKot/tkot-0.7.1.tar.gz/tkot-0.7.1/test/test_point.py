import unittest
from copy import copy
from tKot.common import Point, Polygon


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

    def test_copy(self):
        p = Point(10, 10)
        p2 = copy(p)
        print(id(p2), id(p))

    def test_Polygon(self):
        pol = Polygon(1, 0, 2, 0)
        point = Point(3, 5)
        pol *= 2
        pol += point
        print(*pol)
