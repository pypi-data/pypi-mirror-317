import pytest
from Заур__Илья.Заур__Илья.радиус import circle_area, rectangle_area
import math


def test_circle_area():
    assert abs(circle_area(1) - math.pi) < 1e-10
    assert abs(circle_area(2) - 4 * math.pi) < 1e-10

    with pytest.raises(ValueError):
        circle_area(-1)


def test_rectangle_area():
    assert rectangle_area(2, 3) == 6
    assert rectangle_area(1.5, 2.5) == 3.75

    with pytest.raises(ValueError):
        rectangle_area(-1, 5)