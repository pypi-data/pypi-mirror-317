import math

class Calculator:
    """Simple Calculator for basic arithmetic operations."""

    @staticmethod
    def add(a, b):
        """Add two numbers."""
        return a + b

    @staticmethod
    def subtract(a, b):
        """Subtract two numbers."""
        return a - b

    @staticmethod
    def multiply(a, b):
        """Multiply two numbers."""
        return a * b

    @staticmethod
    def divide(a, b):
        """Divide a by b. Raises ZeroDivisionError if b is zero."""
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed.")
        return a / b

    @staticmethod
    def square_root(a):
        """Return the square root of a number."""
        if a < 0:
            raise ValueError("Cannot compute the square root of a negative number.")
        return math.sqrt(a)

    @staticmethod
    def power(a, b):
        """Return a raised to the power of b."""
        return math.pow(a, b)
