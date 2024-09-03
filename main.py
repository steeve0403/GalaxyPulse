from kivy.app import App
from kivy.graphics import Color, Line
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget


class MainWidget(Widget):
    point_perspective_x = NumericProperty(0)
    point_perspective_y = NumericProperty(0)

    V_NB_LINES = 7  # Preserves symmetry => Use odd number
    V_LINES_SPACING = .1  # percentage in screen width
    vertical_lines = []

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        print("Init W:" + str(self.width) + "H:" + str(self.height))
        self.init_vertical_lines()

    def on_parent(self, widget, parent):
        print("Init W:" + str(self.width) + "H:" + str(self.height))

    def on_size(self, *args):
        self.update_vertical_lines()
        # print("Init W:" + str(self.width) + "H:" + str(self.height))
        # self.point_perspective_x = self.width / 2
        # self.point_perspective_y = self.height / 0.75

    def on_point_perspective_x(self, widget, value):
        # print(f"PX: {str(value)}")
        pass

    def on_point_perspective_y(self, widget, value):
        # print(f"PY: {str(value)}")
        pass

    def init_vertical_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            # self.line = Line(points=[100, 0, 100, 100])
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def update_vertical_lines(self):
        central_line_x = self.width / 2
        spacing = self.V_LINES_SPACING * self.width
        offset = -int(self.V_NB_LINES / 2)
        for i in range(0, self.V_NB_LINES):
            line_x = int(central_line_x + offset * spacing)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)

            self.vertical_lines[i].points = [x1, y1, x2, y2]
            offset += 1

    def transform(self, x, y):
        # return self.transform_2D(x, y)
        return self.transform_perspective(x, y)

    def transform_2D(self, x, y):
        return x, y

    def transform_perspective(self, x, y):
        tr_y = y * self.point_perspective_y / self.height
        if tr_y > self.point_perspective_x:
            tr_y = self.point_perspective_y

        diff_x = x - self.point_perspective_x
        diff_y = self.point_perspective_y - tr_y
        offset_x = diff_x * diff_y / self.point_perspective_y

        tr_x = self.point_perspective_x + offset_x
        return tr_x, tr_y


class GalaxyApp(App):
    pass


GalaxyApp().run()
