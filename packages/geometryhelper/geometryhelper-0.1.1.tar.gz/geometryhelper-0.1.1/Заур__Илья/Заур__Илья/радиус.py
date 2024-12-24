import math


def circle_area(radius: float) -> float:
    """Вычисляет площадь круга"""
    if radius < 0:
        raise ValueError("Радиус не может быть отрицательным")
    return math.pi * radius ** 2


def rectangle_area(length: float, width: float) -> float:
    """Вычисляет площадь прямоугольника"""
    if length <= 0 or width <= 0:
        raise ValueError("Длина и ширина должны быть положительными")
    return length * width