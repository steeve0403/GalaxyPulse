def transform(self, x, y):
    # return self.transform_2D(x, y)
    return self.transform_perspective(x, y)


def transform_2D(self, x, y):
    return int(x), int(y)


def transform_perspective(self, x, y):
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
