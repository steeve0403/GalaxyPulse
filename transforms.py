"""
    This module contains functions to handle 2D and perspective transformations.
"""


def transform(self, x, y):
    """
    Apply 3D transformation to coordinates.

    Args:
        x (float): X-coordinate.
        y (float): Y-coordinate.
        z (float): Z-coordinate.

    Returns:
        tuple: Transformed (x, y, z) coordinates.
    """
    # return self.transform_2D(x, y)
    return self.transform_perspective(x, y)


def transform_2D(self, x, y):
    """
    Apply 2D transformation to coordinates.

    Args:
        x (float): X-coordinate.
        y (float): Y-coordinate.

    Returns:
        tuple: Transformed (x, y) coordinates.
    """
    return int(x), int(y)


def transform_perspective(self, x, y):
    """
    Apply perspective transformation to coordinates.

    Args:
        x (float): X-coordinate.
        y (float): Y-coordinate.
        perspective (float): Perspective value.

    Returns:
        tuple: Transformed coordinates with perspective applied.
    """
    linear_y = y * self.point_perspective_y / self.height
    if linear_y > self.point_perspective_y:
        linear_y = self.point_perspective_y

    diff_x = x - self.point_perspective_x
    diff_y = self.point_perspective_y - linear_y
    factor_y = diff_y / self.point_perspective_y
    factor_y = pow(factor_y, 4)

    offset_x = diff_x * factor_y

    tr_x = self.point_perspective_x + offset_x
    tr_y = self.point_perspective_y - factor_y * self.point_perspective_y

    return int(tr_x), int(tr_y)
