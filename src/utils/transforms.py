def transform(widget, x, y):
    # return self.transform_2D(x, y)
    return transform_perspective(widget, x, y)

def transform_2D(widget, x, y):
    return int(x), int(y)

def transform_perspective(widget, x, y):
    linear_y = y * widget.point_perspective_y / widget.height
    if linear_y > widget.point_perspective_y:
        linear_y = widget.point_perspective_y

    diff_x = x - widget.point_perspective_x
    diff_y = widget.point_perspective_y - linear_y
    factor_y = diff_y / widget.point_perspective_y
    factor_y = pow(factor_y, 4)

    offset_x = diff_x * factor_y

    tr_x = widget.point_perspective_x + offset_x
    tr_y = widget.point_perspective_y - factor_y * widget.point_perspective_y
    return int(tr_x), int(tr_y)