"""
    This module defines functions that respond to user keyboard and touch events.
"""
from kivy.uix.relativelayout import RelativeLayout


def keyboard_closed(self):
    """
        Handle event when the keyboard is closed.
    """
    self.keyboard.unbind(on_key_down=self.on_keyboard_down)
    self.keyboard.bind(on_key_up=self.on_keyboard_up)
    self.keyboard = None


def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    """
        Handle event when a key is pressed.
    """
    if keycode[1] == 'left':
        self.current_speed_x = self.SPEED_X
    elif keycode[1] == 'right':
        self.current_speed_x = -self.SPEED_X
    return True


def on_keyboard_up(self, keyboard, keycode):
    """
        Handle event when a key is released.
    """
    self.current_speed_x = 0


def on_touch_down(self, touch):
    """
    Handle event when a screen touch is detected.

    Args:
        touch (Touch): The touch event.
    """
    if not self.state_game_over and self.state_game_has_started:
        if touch.x < self.width / 2:
            self.current_speed_x = self.SPEED_X
        else:
            self.current_speed_x = -self.SPEED_X
    return super(RelativeLayout, self).on_touch_down(touch)


def on_touch_up(self, touch):
    """
   Handle event when a screen touch ends.

   Args:
       touch (Touch): The touch event.
   """
    pass
