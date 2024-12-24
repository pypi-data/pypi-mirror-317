from typing import Union, Tuple


def solve_quadratic(a: float, b: float, c: float) -> Union[Tuple[float, float], Tuple[float], None]:
    """Решает квадратное уравнение ax² + bx + c = 0"""
    if a == 0:
        raise ValueError("Коэффициент 'a' не может быть равен нулю")

    discriminant = b ** 2 - 4 * a * c

    if discriminant > 0:
        x1 = (-b + discriminant ** 0.5) / (2 * a)
        x2 = (-b - discriminant ** 0.5) / (2 * a)
        return (x1, x2)
    elif discriminant == 0:
        x = -b / (2 * a)
        return (x,)
    else:
        return None