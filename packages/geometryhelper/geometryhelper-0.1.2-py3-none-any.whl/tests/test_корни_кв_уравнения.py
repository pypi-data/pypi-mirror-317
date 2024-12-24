import pytest
from Заур__Илья.Заур__Илья.корни_кв_уравнения import solve_quadratic


def test_solve_quadratic():
    # x² - 1 = 0
    assert set(solve_quadratic(1, 0, -1)) == {1, -1}

    # x² + 2x + 1 = 0
    assert solve_quadratic(1, 2, 1) == (-1,)

    # x² + 1 = 0
    assert solve_quadratic(1, 0, 1) is None

    with pytest.raises(ValueError):
        solve_quadratic(0, 1, 1)