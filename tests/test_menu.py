import pytest
from unittest.mock import MagicMock
from menu import MenuWidget

class TestMenuWidget:

    def setup_method(self):
        """Prépare le menu principal pour chaque test."""
        self.menu_widget = MenuWidget()

    def test_on_touch_down_opacity_zero(self):
        """Test that on_touch_down returns False when opacity is 0."""
        self.menu_widget.opacity = 0
        touch = MagicMock()
        result = self.menu_widget.on_touch_down(touch)
        assert result is False, "The touch should be ignored when opacity is 0."

    def test_on_touch_down_opacity_non_zero(self, mocker):
        """Test that on_touch_down calls the parent method when opacity is non-zero."""
        self.menu_widget.opacity = 1
        touch = MagicMock()
        parent_mock = MagicMock()
        self.menu_widget.on_touch_down = parent_mock
        self.menu_widget.on_touch_down(touch)
        parent_mock.assert_called_once_with(touch)