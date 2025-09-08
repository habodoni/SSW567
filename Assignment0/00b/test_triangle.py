import unittest
import importlib.util
import os


spec = importlib.util.spec_from_file_location(
    "triangle",
    os.path.join(os.path.dirname(__file__), "triangle.py"),
)
triangle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(triangle)
classify_triangle = triangle.classify_triangle

class TestTriangles(unittest.TestCase):

    def test_equilateral(self):
        self.assertEqual(classify_triangle(3, 3, 3), "Equilateral")

    def test_isosceles(self):
        self.assertEqual(classify_triangle(5, 5, 3), "Isosceles")

    def test_scalene(self):
        self.assertEqual(classify_triangle(4, 5, 6), "Scalene")

    def test_right(self):
        self.assertEqual(classify_triangle(3, 4, 5), "Right")

    def test_isosceles_right(self):
        # 1,1,sqrt(2) should be an isosceles right triangle
        import math

        self.assertEqual(classify_triangle(1, 1, math.sqrt(2)), "Isosceles Right")

    def test_float_right_tolerance(self):
        # Large floats that should still detect a right triangle
        self.assertEqual(classify_triangle(3000000.0, 4000000.0, 5000000.0), "Right")

    def test_not_a_triangle(self):
        self.assertEqual(classify_triangle(1, 2, 3), "Not a triangle")

    def test_non_positive(self):
        self.assertEqual(classify_triangle(0, 1, 1), "Not a triangle")
        self.assertEqual(classify_triangle(-1, 2, 2), "Not a triangle")

if __name__ == '__main__':
    unittest.main()