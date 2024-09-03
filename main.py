from kivy.app import App
from kivy.properties import NumericProperty
from kivy.uix.widget import Widget


class MainWidget(Widget):
    point_perspective_x = NumericProperty(0)
    point_perspective_y = NumericProperty(0)

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        print("Init W:" + str(self.width) + "H:" + str(self.height))

    def on_parent(self, widget, parent):
        print("Init W:" + str(self.width) + "H:" + str(self.height))

    def on_size(self, *args):
        pass
        # print("Init W:" + str(self.width) + "H:" + str(self.height))
        # self.point_perspective_x = self.width / 2
        # self.point_perspective_y = self.height / 0.75

    def on_point_perspective_x(self, widget, value):
        # print(f"PX: {str(value)}")
        pass
    def on_point_perspective_y(self, widget, value):
        # print(f"PY: {str(value)}")
        pass

class GalaxyApp(App):
    pass


GalaxyApp().run()
