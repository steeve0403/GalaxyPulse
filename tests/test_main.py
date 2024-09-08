import pytest
import pytest
from kivy.clock import Clock
from main import MainWidget, Triangle

class TestGame:

    def setup_method(self):
        """Prepares a new game state before each test."""
        self.game = MainWidget()

    def test_init_ship(self):
        """Test l'initialisation correcte du vaisseau."""
        assert hasattr(self.game, 'ship'), "The ship has not been initialized."
        assert isinstance(self.game.ship, Triangle), "The ship object is not a Triangle."

    # def test_update_ship(self):
    #     """Test the update of the vessel position."""
    #     initial_pos = self.game.ship.points
    #     self.game.point_perspective_y = 1
    #     self.game.update(1.0)
    #     assert self.game.ship.opacity == initial_pos
    #     assert self.game.ship.points != initial_pos, "The position of the ship has not changed after the update."

    def test_collision_ship_obstacle(self):
        """Test the detection of collision between the vessel and an obstacle."""
        self.game.ship.points = [100, 100, 110, 100, 105, 110]
        self.game.obstacles = [(100, 100)]
        self.game.check_ship_collision()
        assert self.game.state_game_over != True, "The collision was not detected correctly."

    def test_restart_game(self):
        """Test the game reset after a game."""
        self.game.state_game_over = True
        self.game.reset_game()
        assert self.game.state_game_over == False, "The game did not reset properly."
        assert self.game.ship.points == [0.0, 0.0, 100.0, 0.0, 50.0, 100.0], "The ship’s position has not been reset."
