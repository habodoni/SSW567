"""Simple triangle classifier for homework.

Given three side lengths, return a short label for the triangle type.
"""

import math


def classify_triangle(a, b, c):
    """Classify a triangle by side lengths a, b, c.

    Returns one of: 'Not a triangle', 'Equilateral', 'Isosceles Right',
    'Right', 'Isosceles', or 'Scalene'.
    """

    result = None

    # Reject non-positive side lengths
    if a <= 0 or b <= 0 or c <= 0:
        result = "Not a triangle"
    # Check the triangle inequality
    elif a + b <= c or a + c <= b or b + c <= a:
        result = "Not a triangle"
    # Check for equilateral
    elif a == b == c:
        result = "Equilateral"
    else:
    # Right triangle check (Pythagoras with a tiny tolerance)
        sides = sorted([a, b, c])
        if math.isclose(
            sides[0] ** 2 + sides[1] ** 2,
            sides[2] ** 2,
            rel_tol=1e-9,
            abs_tol=1e-9,
        ):
            if a == b or b == c or a == c:
                result = "Isosceles Right"
            else:
                result = "Right"
    # Isosceles check
        elif a == b or b == c or a == c:
            result = "Isosceles"
        else:
            # If none of the above, it's scalene
            result = "Scalene"

    return result
