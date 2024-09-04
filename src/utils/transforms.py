def transform(widget, x, y):
    # return self.transform_2D(x, y)
    return transform_perspective(widget, x, y)

def transform_2D(widget, x, y):
    return int(x), int(y)

def transform_perspective(self, x, y):
    linear_y = y * self.point_perspective_y / self.height
    linear_y = min(linear_y, self.point_perspective_y)  # Limiter la valeur maximale

    diff_x = x - self.point_perspective_x
    diff_y = self.point_perspective_y - linear_y
    factor_y = (diff_y / self.point_perspective_y) ** 4  # Éviter plusieurs appels à pow()

    offset_x = diff_x * factor_y
    tr_x = self.point_perspective_x + offset_x
    tr_y = self.point_perspective_y - factor_y * self.point_perspective_y
    return int(tr_x), int(tr_y)