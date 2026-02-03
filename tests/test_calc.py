import pytest

from jenkins_practice.calc import add, div, mul, sub


def test_add():
    assert add(2, 3) == 5


def test_sub():
    assert sub(10, 4) == 6


def test_mul():
    assert mul(6, 7) == 42


def test_div():
    assert div(8, 2) == 4


def test_div_by_zero_raises():
    with pytest.raises(ZeroDivisionError):
        div(1, 0)
