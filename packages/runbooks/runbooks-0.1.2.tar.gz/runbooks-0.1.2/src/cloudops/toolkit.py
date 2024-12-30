from typing import Tuple, Union

from loguru import logger

## Define a type alias for supported numeric types
Number = Union[float, int]


def add(a: Number, b: Number) -> float:
    """Compute and return the sum of two numbers.

    Examples:
        >>> add(4.0, 2.0)
        6.0
        >>> add(4, 2)
        6.0

    Args:
        a: The first number in the addition.
        b: The second number in the addition.

    Returns:
        float: The arithmetic sum of `a` and `b`.

    Raises:
        TypeError: If inputs are not numbers.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both inputs must be integers or floats.")

    logger.debug(f"Adding {a} + {b}")
    return float(a + b)


def subtract(a: Number, b: Number) -> float:
    """Compute and return the subtraction of two numbers.

    Examples:
        >>> subtract(4.0, 2.0)
        2.0
        >>> subtract(4, 2)
        2.0

    Args:
        a: The first number in the subtraction.
        b: The second number in the subtraction.

    Returns:
        float: The arithmetic subtraction of `a` and `b`.

    Raises:
        TypeError: If inputs are not numbers.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both inputs must be integers or floats.")

    logger.debug(f"Subtracting {a} - {b}")
    return float(a - b)


def multiply(a: Number, b: Number) -> float:
    """Compute and return the multiplication of two numbers.

    Examples:
        >>> multiply(4.0, 2.0)
        8.0
        >>> multiply(4, 2)
        8.0

    Args:
        a: The first number in the multiplication.
        b: The second number in the multiplication.

    Returns:
        float: The arithmetic multiplication of `a` and `b`.

    Raises:
        TypeError: If inputs are not numbers.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both inputs must be integers or floats.")

    logger.debug(f"Multiplying {a} * {b}")
    return float(a * b)


def divide(a: Number, b: Number) -> float:
    """Compute and return the division of two numbers.

    Examples:
        >>> divide(4.0, 2.0)
        2.0
        >>> divide(4, 2)
        2.0

    Args:
        a: The numerator.
        b: The denominator.

    Returns:
        float: The result of dividing `a` by `b`.

    Raises:
        TypeError: If inputs are not numbers.
        ZeroDivisionError: If the denominator is zero.
    """
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both inputs must be integers or floats.")
    if b == 0:
        logger.error("Attempted division by zero.")
        raise ZeroDivisionError("division by zero")

    logger.debug(f"Dividing {a} / {b}")
    return float(a / b)


def divide(a: Number, b: Number) -> float:
    """Compute and return the division of two numbers.

    Examples:
        >>> divide(4.0, 2.0)
        2.0
        >>> divide(4, 2)
        2.0

    Args:
        a: The numerator.
        b: The denominator.

    Returns:
        float: The result of dividing `a` by `b`.

    Raises:
        TypeError: If inputs are not numbers.
        ZeroDivisionError: If the denominator is zero.
    """
    # Input validation
    if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
        raise TypeError("Both inputs must be integers or floats.")

    # Handle division by zero
    if b == 0:
        raise ZeroDivisionError("division by zero")

    # Perform division
    logger.debug(f"Dividing {a} / {b}")
    return float(a / b)
