import unittest
from io import StringIO
import sys
from pattern_sort.pattern import Pattern

class TestPattern(unittest.TestCase):
    def setUp(self):
        self.pattern = Pattern()

    def capture_output(self, func, *args, **kwargs):
        """Utility function to capture printed output."""
        captured_output = StringIO()
        sys.stdout = captured_output
        func(*args, **kwargs)
        sys.stdout = sys.__stdout__
        return captured_output.getvalue().strip()

    def test_print_triangle(self):
        result = self.capture_output(self.pattern.print_triangle, 3)
        self.assertEqual(result, "*\n**\n***")

    def test_print_reverse_triangle(self):
        result = self.capture_output(self.pattern.print_reverse_triangle, 3)
        self.assertEqual(result, "***\n**\n*")

    def test_print_pyramid(self):
        result = self.capture_output(self.pattern.print_pyramid, 3)
        self.assertEqual(result, "  *\n ***\n*****")

    def test_print_diamond(self):
        result = self.capture_output(self.pattern.print_diamond, 3)
        self.assertEqual(result, "  *\n ***\n*****\n ***\n  *")

    def test_print_square(self):
        result = self.capture_output(self.pattern.print_square, 3)
        self.assertEqual(result, "***\n***\n***")

    def test_print_hollow_square(self):
        result = self.capture_output(self.pattern.print_hollow_square, 3)
        self.assertEqual(result, "***\n* *\n***")

    def test_print_right_triangle(self):
        result = self.capture_output(self.pattern.print_right_triangle, 3)
        self.assertEqual(result, "  *\n **\n***")

    def test_print_hollow_triangle(self):
        result = self.capture_output(self.pattern.print_hollow_triangle, 4)
        self.assertEqual(result, "*\n**\n* *\n****")

    def test_print_checkerboard(self):
        result = self.capture_output(self.pattern.print_checkerboard, 3, 3)
        self.assertEqual(result, "* *\n * \n* *")

    def test_print_zigzag(self):
        result = self.capture_output(self.pattern.print_zigzag, 3, 5)
        self.assertEqual(result, "* * *\n * * \n* * *")

if __name__ == "__main__":
    unittest.main()
