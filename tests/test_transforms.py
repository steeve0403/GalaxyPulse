import pytest
from transforms import transform_2D, transform_perspective


class MockTransform:
    point_perspective_x = 200
    point_perspective_y = 150
    height = 400


def test_transform_2D():
    mock = MockTransform()
    # Test de base pour transform_2D
    result = transform_2D(mock, 100, 200)
    assert result == (100, 200), "La transformation 2D a échoué"


def test_transform_perspective():
    mock = MockTransform()

    result = transform_perspective(mock, 100, 200)

    expected = (193, 140)
    assert result == expected, "La transformation en perspective n'est pas correcte"
