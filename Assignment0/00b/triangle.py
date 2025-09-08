import math


def classify_triangle(a, b, c):
    """Classify a triangle based on side lengths a, b, c."""

    # Reject non-positive side lengths
    if a <= 0 or b <= 0 or c <= 0:
        return "Not a triangle"

    # First check if inputs can form a triangle
    if a + b <= c or a + c <= b or b + c <= a:
        return "Not a triangle"

    # Check for equilateral
    if a == b == c:
        return "Equilateral"

    # Check for right triangle using Pythagoras with tolerance
    sides = sorted([a, b, c])
    if math.isclose(sides[0]**2 + sides[1]**2, sides[2]**2, rel_tol=1e-9, abs_tol=1e-9):
        if a == b or b == c or a == c:
            return "Isosceles Right"
        return "Right"

    # Check for isosceles
    if a == b or b == c or a == c:
        return "Isosceles"

    # If none of the above, it’s scalene
    return "Scalene"