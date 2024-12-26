import unittest
from math_calculator import Calculator


class TestCalculator(unittest.TestCase):

    def test_add(self):
        self.assertEqual(Calculator.add(1, 2), 3)

    def test_subtract(self):
        self.assertEqual(Calculator.subtract(5, 3), 2)

    def test_multiply(self):
        self.assertEqual(Calculator.multiply(2, 3), 6)

    def test_divide(self):
        self.assertEqual(Calculator.divide(6, 2), 3)
        with self.assertRaises(ZeroDivisionError):
            Calculator.divide(6, 0)

    def test_square_root(self):
        self.assertEqual(Calculator.square_root(9), 3)
        with self.assertRaises(ValueError):
            Calculator.square_root(-1)

    def test_power(self):
        self.assertEqual(Calculator.power(2, 3), 8)


if __name__ == '__main__':
    unittest.main()
