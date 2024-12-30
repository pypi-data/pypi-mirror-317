import unittest
from .shape_areas import ShapeArea

class TestArea(unittest.TestCase):
    def setUp(self):
        self.area = ShapeArea()

    def test_square(self):
        self.assertEqual(self.area.square(2), 4.0)
        self.assertEqual(self.area.square(3), 9.0)
        self.assertNotEqual(self.area.square(2),5.0)

    def test_rectangle(self):
        self.assertEqual(self.area.rectangle(2,3), 6.0)
        self.assertEqual(self.area.rectangle(4,3), 12.0)
        self.assertNotEqual(self.area.rectangle(2,3), 7.0)

    def test_circle(self):
        self.assertEqual(self.area.circle(2), 12.57)
        self.assertEqual(self.area.circle(3), 28.27)
        self.assertNotEqual(self.area.circle(2), 13.57)

    def test_triangle(self):
        self.assertEqual(self.area.triangle(2,3), 3.0)
        self.assertEqual(self.area.triangle(4,3), 6.0)
        self.assertNotEqual(self.area.triangle(2,3), 7.0)

    def test_trapezoid(self):
        self.assertEqual(self.area.trapezoid(2,3,4), 10.0)
        self.assertEqual(self.area.trapezoid(4,3,2), 7.0)
        self.assertNotEqual(self.area.trapezoid(2,3,4), 11.0)

    def test_parallelogram(self):
        self.assertEqual(self.area.parallelogram(2,3), 6.0)
        self.assertEqual(self.area.parallelogram(4,3), 12.0)
        self.assertNotEqual(self.area.parallelogram(2,3), 7.0)

    def test_rhombus(self):
        self.assertEqual(self.area.rhombus(2,3), 3.0)
        self.assertEqual(self.area.rhombus(4,3), 6.0)
        self.assertNotEqual(self.area.rhombus(2,3), 7.0)

if __name__ == '__main__':
    unittest.main()