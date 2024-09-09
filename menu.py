"""
This module defines the MenuWidget class which handles the game's menu system.
"""
from kivy.uix.relativelayout import RelativeLayout


class MenuWidget(RelativeLayout):
    """
    MenuWidget manages the main game menu and detects user interactions.
    """


    def on_touch_down(self, touch):
        """
        Handle touch events when the user interacts with the menu.

        Args:
            touch (Touch): The touch event.

        Returns:
            bool: Whether the touch was handled by the menu.
        """
        if self.opacity == 0:
            return False
        return super(RelativeLayout, self).on_touch_down(touch)
