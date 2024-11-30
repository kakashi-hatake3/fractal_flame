import pytest
from src.variations import Variations


@pytest.mark.parametrize("x, y, expected_x, expected_y", [
    (1, 2, 1, 2),
    (0, 0, 0, 0),
])
def test_linear(x, y, expected_x, expected_y):
    result_x, result_y = Variations.linear(x, y)
    assert result_x == expected_x
    assert result_y == expected_y


@pytest.mark.parametrize("x, y", [
    (1, 2),
    (3, -1),
])
def test_sinusoidal(x, y):
    result_x, result_y = Variations.sinusoidal(x, y)
    assert isinstance(result_x, float)
    assert isinstance(result_y, float)


@pytest.mark.parametrize("x, y", [
    (1, 1),
    (2, -2),
])
def test_spherical(x, y):
    result_x, result_y = Variations.spherical(x, y)
    assert isinstance(result_x, float)
    assert isinstance(result_y, float)


@pytest.mark.parametrize("x, y", [
    (1, 1),
    (0.5, 0.5),
])
def test_swirl(x, y):
    result_x, result_y = Variations.swirl(x, y)
    assert isinstance(result_x, float)
    assert isinstance(result_y, float)


@pytest.mark.parametrize("x, y", [
    (1, 1),
    (0.5, -0.5),
])
def test_polar(x, y):
    result_x, result_y = Variations.polar(x, y)
    assert isinstance(result_x, float)
    assert isinstance(result_y, float)


@pytest.mark.parametrize("x, y", [
    (1, 1),
    (2, -2),
])
def test_cosine(x, y):
    result_x, result_y = Variations.cosine(x, y)
    assert isinstance(result_x, float)
    assert isinstance(result_y, float)
