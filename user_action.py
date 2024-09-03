def keyboard_closed(self):
    self.keyboard.unbind(on_key_down=self.on_keyboard_down)
    self.keyboard.bind(on_key_up=self.on_keyboard_up)
    self.keyboard = None


def on_keyboard_up(self, keyboard, keycode):
    self.current_speed_x = 0


def on_touch_down(self, touch):
    if touch.x < self.width / 2:
        self.current_speed_x = self.SPEED_X
    else:
        self.current_speed_x = -self.SPEED_X


def on_touch_up(self, touch):
    pass
