import pytest
from transforms import transform_2D, transform_perspective


class MockTransform:
    point_perspective_x = 200
    point_perspective_y = 150
    height = 400


def test_transform_2D():
    mock = MockTransform()
    result = transform_2D(mock, 100, 200)
    assert result == (100, 200), "2D transformation failed"


def test_transform_perspective():
    mock = MockTransform()

    result = transform_perspective(mock, 100, 200)

    expected = (193, 140)
    assert result == expected, "The perspective transformation is not correct"
