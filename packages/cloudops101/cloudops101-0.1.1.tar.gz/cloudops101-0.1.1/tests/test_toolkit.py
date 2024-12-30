import sys
from pathlib import Path

# Add the src directory to the Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

import pytest

from cloudops.toolkit import add, divide, multiply, subtract

#################################################################################
# TEST CASES: ADDITION                                                          #
#################################################################################


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 5.0),  # Integer addition
        (2.5, 3.5, 6.0),  # Float addition
        (-1, 1, 0.0),  # Negative and positive numbers
        (0, 0, 0.0),  # Zero addition
        (1e10, 1e10, 2e10),  # Large numbers
    ],
)
def test_add(a, b, expected):
    """Test add function with various inputs."""
    assert add(a, b) == expected


#################################################################################
# TEST CASES: SUBTRACTION                                                       #
#################################################################################


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (5, 3, 2.0),  # Integer subtraction
        (2.5, 1.5, 1.0),  # Float subtraction
        (-1, -1, 0.0),  # Negative numbers
        (0, 0, 0.0),  # Zero subtraction
        (1e10, 1e5, 9.9999e9),  # Large numbers
    ],
)
def test_subtract(a, b, expected):
    """Test subtract function with various inputs."""
    assert subtract(a, b) == expected


#################################################################################
# TEST CASES: MULTIPLICATION                                                    #
#################################################################################


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (2, 3, 6.0),  # Integer multiplication
        (2.5, 4, 10.0),  # Float multiplication
        (-2, 3, -6.0),  # Negative numbers
        (0, 5, 0.0),  # Zero multiplication
        (1e5, 1e5, 1e10),  # Large numbers
    ],
)
def test_multiply(a, b, expected):
    """Test multiply function with various inputs."""
    assert multiply(a, b) == expected


#################################################################################
# TEST CASES: DIVISION                                                          #
#################################################################################


@pytest.mark.parametrize(
    "a, b, expected",
    [
        (6, 3, 2.0),  # Integer division
        (2.5, 0.5, 5.0),  # Float division
        (-6, 3, -2.0),  # Negative numbers
        (1e10, 1e5, 1e5),  # Large numbers
    ],
)
def test_divide(a, b, expected):
    """Test divide function with valid inputs."""
    assert divide(a, b) == expected


#################################################################################
# EDGE CASES: DIVISION BY ZERO                                                  #
#################################################################################


def test_divide_by_zero():
    """Test divide function raises ZeroDivisionError on zero divisor."""
    with pytest.raises(ZeroDivisionError, match="division by zero"):
        divide(10, 0)


#################################################################################
# EDGE CASES: INVALID INPUTS                                                    #
#################################################################################


@pytest.mark.parametrize(
    "func, a, b",
    [
        (add, "a", 1),  # Non-numeric input
        (subtract, 1, "b"),  # Non-numeric input
        (multiply, "a", "b"),  # Non-numeric inputs
        (divide, None, 1),  # None as input
    ],
)
def test_invalid_inputs(func, a, b):
    """Test functions with invalid inputs."""
    with pytest.raises(TypeError):
        func(a, b)


#################################################################################
# PERFORMANCE TEST CASES                                                        #
#################################################################################


def test_large_operations():
    """Test functions with extremely large numbers."""
    big_num = 1e100
    assert add(big_num, big_num) == 2e100
    assert subtract(big_num, big_num) == 0.0
    assert multiply(big_num, 2) == 2e100
    assert divide(big_num, 1) == big_num


#################################################################################
# FINAL TEST FOR FUNCTION RETURN TYPES                                          #
#################################################################################


@pytest.mark.parametrize(
    "func, a, b",
    [
        (add, 1, 2),
        (subtract, 5, 3),
        (multiply, 2, 3),
        (divide, 6, 2),
    ],
)
def test_return_type(func, a, b):
    """Test if the return type of all functions is float."""
    assert isinstance(func(a, b), float)
