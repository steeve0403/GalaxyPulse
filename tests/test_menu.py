import pytest
from unittest.mock import MagicMock
from menu import MenuWidget

class TestMenuWidget:

    def setup_method(self):
        """Prépare le menu principal pour chaque test."""
        self.menu_widget = MenuWidget()

    def test_on_touch_down_opacity_zero(self):
        """Test que on_touch_down retourne False quand l'opacité est à 0."""
        self.menu_widget.opacity = 0

        # Simuler un touch en utilisant MagicMock pour remplacer MotionEvent
        touch = MagicMock()

        # Vérifie que la fonction retourne False quand l'opacité est 0
        result = self.menu_widget.on_touch_down(touch)
        assert result is False, "Le touch doit être ignoré lorsque l'opacité est 0."

    def test_on_touch_down_opacity_non_zero(self, mocker):
        """Test que on_touch_down appelle la méthode parent quand l'opacité est non-nulle."""
        self.menu_widget.opacity = 1

        # Simuler un touch en utilisant MagicMock pour remplacer MotionEvent
        touch = MagicMock()

        parent_mock = MagicMock()
        self.menu_widget.on_touch_down = parent_mock

        # Appeler la méthode on_touch_down
        self.menu_widget.on_touch_down(touch)

        # Vérifier que la méthode parent a bien été appelée
        parent_mock.assert_called_once_with(touch)