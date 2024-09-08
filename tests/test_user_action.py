from kivy.uix.relativelayout import RelativeLayout


class MockGame(RelativeLayout):
    SPEED_X = 10
    current_speed_x = 0
    state_game_over = False
    state_game_has_started = True

    def on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'left':
            self.current_speed_x = self.SPEED_X
        elif keycode[1] == 'right':
            self.current_speed_x = -self.SPEED_X
        return True

    def on_keyboard_up(self, keyboard, keycode):
        self.current_speed_x = 0
        return True

    def on_touch_down(self, touch):
        if not self.state_game_over and self.state_game_has_started:
            if touch.x < self.width / 2:
                self.current_speed_x = self.SPEED_X
            else:
                self.current_speed_x = -self.SPEED_X
        return True

    def on_touch_up(self, touch):
        return None


class TestUserActions:
    def test_on_keyboard_down_left_arrow(self):
        game = MockGame()

        keycode = (276, 'left')
        text = "left"
        modifiers = []

        game.on_keyboard_down(None, keycode, text, modifiers)

        assert game.current_speed_x == game.SPEED_X, "Pressing the left arrow did not trigger correct movement"

    def test_on_keyboard_down_right_arrow(self):
        game = MockGame()

        keycode = (275, 'right')
        text = "right"
        modifiers = []

        game.on_keyboard_down(None, keycode, text, modifiers)

        assert game.current_speed_x == -game.SPEED_X, "Pressing the right arrow did not trigger correct movement"

    def test_on_keyboard_up(self):
        game = MockGame()
        keycode = (275, 'right')
        game.on_keyboard_down(None, keycode, "right", [])

        assert game.current_speed_x == -game.SPEED_X

        game.on_keyboard_up(None, keycode)

        assert game.current_speed_x == 0, "Speed was not reset after release of key"

    def test_on_touch_down(self):
        game = MockGame()
        game.width = 500

        class MockTouch:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        touch = MockTouch(100, 200)
        game.on_touch_down(touch)

        assert game.current_speed_x == game.SPEED_X, "Left click did not trigger correct movement"

    def test_on_touch_up(self):
        game = MockGame()

        class MockTouch:
            def __init__(self, x, y):
                self.x = x
                self.y = y

        touch = MockTouch(100, 200)
        result = game.on_touch_up(touch)

        assert result is None, "The on_touch_up method should return None"
