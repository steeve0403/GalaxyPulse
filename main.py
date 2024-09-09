from kivy.config import Config
from kivy.core.audio import SoundLoader
from kivy.uix.relativelayout import RelativeLayout

"""
This module contains the core game functionality, including rendering, player movement, and interaction with the game environment.
"""
# Config.set('graphics', 'width', '900')
# Config.set('graphics', 'height', '550')

import random
from kivy.core.window import Window
from kivy import platform
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import Color, Line, Quad, Triangle
from kivy.properties import NumericProperty, Clock, ObjectProperty, StringProperty

Builder.load_file('menu.kv')


class MainWidget(RelativeLayout):
    """
    MainWidget handles the main gameplay area, player controls, and rendering.
    Attributes:
        menu_widget (ObjectProperty): Menu displayed when game is paused or over.
        point_perspective_x (NumericProperty): X-coordinate for perspective transformation.
        point_perspective_y (NumericProperty): Y-coordinate for perspective transformation.
        V_NB_LINES (int): Number of vertical lines.
        H_NB_LINES (int): Number of horizontal lines.
        SPEED (float): Speed at which the background scrolls.
        SHIP_WIDTH (float): Width of the player's ship.
        state_game_over (bool): Game over state.
        state_game_has_started (bool): Whether the game has started.
    """

    from transforms import transform, transform_2D, transform_perspective
    from user_action import keyboard_closed, on_keyboard_up, on_keyboard_down, on_touch_down, on_touch_up

    menu_widget = ObjectProperty()
    point_perspective_x = NumericProperty(0)
    point_perspective_y = NumericProperty(0)

    # Vertical Lines
    V_NB_LINES = 8  # Symmetry is preserved => Use odd number
    V_LINES_SPACING = .4  # percentage in screen width
    vertical_lines = []

    # Horizontal lines
    H_NB_LINES = 8
    H_LINES_SPACING = .15  # percentage in screen width
    horizontal_lines = []

    SPEED = .8
    current_offset_y = 0
    current_y_loop = 0

    SPEED_X = 3.5
    current_speed_x = 0
    current_offset_x = 0

    NB_TILES = 16
    tiles = []
    tiles_coordinates = []

    SHIP_WIDTH = .1
    SHIP_HEIGHT = 0.035
    SHIP_BASE_Y = 0.04
    ship = None
    ship_coordinates = [(0, 0), (0, 0), (0, 0)]

    state_game_over = False
    state_game_has_started = False

    menu_title = StringProperty("G A L A X Y")
    menu_button_title = StringProperty("Start")

    score_txt = StringProperty()

    sound_begin = None
    sound_galaxy = None
    sound_game_over_impact = None
    sound_game_over_voice = None
    sound_music1 = None
    sound_restart = None

    def __init__(self, **kwargs):
        """
        Initialize the MainWidget and set up all initial game parameters.
        Sets the default layout, initial speed, and tile positions.
        """
        super(MainWidget, self).__init__(**kwargs)
        self.init_audio()
        self.init_vertical_lines()
        self.init_horizontal_lines()
        self.init_tiles()
        self.init_ship()
        self.reset_game()

        if self.is_desktop():
            self.keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self.keyboard.bind(on_key_down=self.on_keyboard_down)
            self.keyboard.bind(on_key_up=self.on_keyboard_up)
        Clock.schedule_interval(self.update, 1.0 / 60.0)

        self.sound_galaxy.play()

    def init_audio(self):
        """
        Initialize the audio files used in the game, including background music and sound effects.
        """
        self.sound_begin = SoundLoader.load('audio/begin.wav')
        self.sound_galaxy = SoundLoader.load('audio/galaxy.wav')
        self.sound_game_over_impact = SoundLoader.load('audio/gameover_impact.wav')
        self.sound_game_over_voice = SoundLoader.load('audio/gameover_voice.wav')
        self.sound_music1 = SoundLoader.load('audio/music1.wav')
        self.sound_restart = SoundLoader.load('audio/restart.wav')

        self.sound_music1.volume = 1
        self.sound_begin.volume = .25
        self.sound_galaxy.volume = .25
        self.sound_game_over_voice.volume = .25
        self.sound_restart.volume = .25
        self.sound_game_over_impact.volume = .6

    def reset_game(self):
        """
        Reset the game state to the starting point. This includes resetting the player's position, score, and game environment.
        """
        self.current_offset_y = 0
        self.current_y_loop = 0
        self.current_speed_x = 0
        self.current_offset_x = 0
        self.score_txt = "Score: " + str(self.current_y_loop)

        self.tiles_coordinates = []
        self.pre_fill_tiles_coordinates()
        self.generate_tiles_coordinates()
        self.state_game_over = False

    def is_desktop(self):
        """
        Check if the current platform is a desktop environment (Linux, Windows, macOS).

        Returns:
            bool: True if running on a desktop platform, False otherwise.
        """
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False

    def init_ship(self):
        """
        Initialize the player's ship with default size and position.
        """
        with self.canvas:
            Color(0, 0, 0)
            self.ship = Triangle()

    def update_ship(self):
        """
        Update the position and transformation of the player's ship based on current coordinates.
        """
        center_x = self.width / 2
        base_y = self.SHIP_BASE_Y * self.height
        half_width = self.SHIP_WIDTH * self.width / 2
        ship_height = self.SHIP_HEIGHT * self.height

        #   2
        # 1  3
        self.ship_coordinates[0] = (center_x - half_width, base_y)
        self.ship_coordinates[1] = (center_x, base_y + ship_height)
        self.ship_coordinates[2] = (center_x + half_width, base_y)

        x1, y1 = self.transform(*self.ship_coordinates[0])
        x2, y2 = self.transform(*self.ship_coordinates[1])
        x3, y3 = self.transform(*self.ship_coordinates[2])

        self.ship.points = [x1, y1, x2, y2, x3, y3]

    def check_ship_collision(self):
        """
        Check if the player's ship has collided with any obstacles (tiles).

        Returns:
            bool: True if a collision occurred, otherwise False.
        """
        for i in range(0, len(self.tiles_coordinates)):
            tile_x, tile_y = self.tiles_coordinates[i]
            if tile_y > self.current_y_loop + 1:
                return False
            if self.check_ship_collision_with_tile(tile_x, tile_y):
                return True
        return False

    def check_ship_collision_with_tile(self, tile_x, tile_y):
        """
        Check if the ship is colliding with a specific tile.

        Args:
            tile_x (int): The x-coordinate of the tile.
            tile_y (int): The y-coordinate of the tile.

        Returns:
            bool: True if the ship is colliding with the tile, False otherwise.
        """
        x_min, y_min = self.get_tile_coordinates(tile_x, tile_y)
        x_max, y_max = self.get_tile_coordinates(tile_x + 1, tile_y + 1)
        for i in range(0, 3):
            p_x, p_y = self.ship_coordinates[i]
            if x_min <= p_x <= x_max and y_min <= p_y <= y_max:
                return True
        return False

    def init_tiles(self):
        """
        Initialize the game's tiles, setting their initial positions on the screen.
        Tiles are the obstacles that the player must navigate through.
        """
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.NB_TILES):
                self.tiles.append(Quad())

    def pre_fill_tiles_coordinates(self):
        """
        Fill the initial set of tiles coordinates.
        """
        for i in range(0, 10):
            self.tiles_coordinates.append((0, i))

    def generate_tiles_coordinates(self):
        """
        Generate new tile coordinates dynamically as the player progresses.
        """
        last_y = 0
        last_x = 0

        for i in range(len(self.tiles_coordinates) - 1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1

        for i in range(len(self.tiles_coordinates), self.NB_TILES):
            r = random.randint(0, 2)
            # 0 -> all right
            # 1 -> right
            # 2 -> left
            start_index = -int(self.V_NB_LINES / 2) + 1
            end_index = start_index + self.V_NB_LINES - 1
            if last_x <= start_index:
                r = 1
            if last_x >= end_index:
                r = 2
            self.tiles_coordinates.append((last_x, last_y))
            if r == 1:
                last_x += 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            if r == 2:
                last_x -= 1
                self.tiles_coordinates.append((last_x, last_y))
                last_y += 1
                self.tiles_coordinates.append((last_x, last_y))
            last_y += 1

    def init_vertical_lines(self):
        """
        Initialize the vertical lines for the background grid, determining spacing and initial positions.
        These lines create the 3D perspective effect.
        """
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.V_NB_LINES):
                self.vertical_lines.append(Line())

    def get_line_x_from_index(self, index):
        """
        Calculate the x-coordinate of a vertical line based on its index.

        Args:
            index (int): The index of the vertical line.

        Returns:
            float: The x-coordinate of the vertical line.
        """
        central_line_x = self.point_perspective_x
        spacing = self.V_LINES_SPACING * self.width
        offset = index - 0.5
        line_x = central_line_x + offset * spacing + self.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        """
        Calculate the y-coordinate of a horizontal line based on its index.

        Args:
            index (int): The index of the horizontal line.

        Returns:
            float: The y-coordinate of the horizontal line.
        """
        spacing_y = self.H_LINES_SPACING * self.height
        line_y = index * spacing_y - self.current_offset_y
        return line_y

    def get_tile_coordinates(self, tile_x, tile_y):
        """
        Get the x and y coordinates of a tile based on its tile indices.

        Args:
            tile_x (int): The x index of the tile.
            tile_y (int): The y index of the tile.

        Returns:
            tuple: The (x, y) coordinates of the tile.
        """
        tile_y = tile_y - self.current_y_loop
        x = self.get_line_x_from_index(tile_x)
        y = self.get_line_y_from_index(tile_y)
        return x, y

    def update_tiles(self):
        """
        Update the position of the tiles based on the player's current position in the game world.
        """
        for i in range(0, self.NB_TILES):
            tile = self.tiles[i]
            tile_coordinates = self.tiles_coordinates[i]

            x_min, y_min = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            x_max, y_max = self.get_tile_coordinates(tile_coordinates[0] + 1, tile_coordinates[1] + 1)

            #   2   3
            #
            #   1   4
            x1, y1 = self.transform(x_min, y_min)
            x2, y2 = self.transform(x_min, y_max)
            x3, y3 = self.transform(x_max, y_max)
            x4, y4 = self.transform(x_max, y_min)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update_vertical_lines(self):
        """
        Update the position of the vertical lines to reflect the current player perspective.
        """
        start_index = -int(self.V_NB_LINES / 2) + 1
        for i in range(start_index, start_index + self.V_NB_LINES):
            line_x = self.get_line_x_from_index(i)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def init_horizontal_lines(self):
        """
        Initialize the horizontal lines for the background grid, determining spacing and initial positions.
        The lines move with the vertical scroll.
        """
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, self.H_NB_LINES):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        """
        Update the position of the horizontal lines to reflect the current player perspective.
        """
        start_index = -int(self.V_NB_LINES / 2) + 1
        end_index = start_index + self.V_NB_LINES - 1

        x_min = self.get_line_x_from_index(start_index)
        x_max = self.get_line_x_from_index(end_index)

        for i in range(0, self.H_NB_LINES):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(x_min, line_y)
            x2, y2 = self.transform(x_max, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def update(self, dt):
        """
        Update the game state at each frame. This function is scheduled to run at intervals and updates the
        position of the background, tiles, and player's ship.

        Args:
            dt (float): Time delta between each update call.
        """
        # print("dt : " + str(dt))
        time_factor = dt * 60

        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()

        if not self.state_game_over and self.state_game_has_started:
            speed_y = self.SPEED * self.height / 100
            self.current_offset_y += speed_y * time_factor

            spacing_y = self.H_LINES_SPACING * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.score_txt = "Score: " + str(self.current_y_loop)
                self.generate_tiles_coordinates()

            speed_x = self.current_speed_x * self.width / 100
            self.current_offset_x += speed_x * time_factor

        if not self.check_ship_collision() and not self.state_game_over:
            self.state_game_over = True
            self.menu_title = "G A M E  O V E R"
            self.menu_title = "Restart"
            self.menu_widget.opacity = 1
            self.sound_music1.stop()
            self.sound_game_over_impact.play()
            Clock.schedule_once(self.play_voice_game_over, 3)
            print("GAME OVER")

    def play_voice_game_over(self, dt):
        """
        Play the game over voice sound effect after a delay when the player loses.
        """
        if self.state_game_over:
            self.sound_game_over_voice.play()

    def on_menu_btn_pressed(self):
        """
        Handle the event when the menu button is pressed. This either starts or restarts the game.
        """
        if self.state_game_over:
            self.sound_restart.play()
        else:
            self.sound_begin.play()
            self.sound_music1.play()
        self.reset_game()
        self.state_game_has_started = True
        self.menu_widget.opacity = 0


class GalaxyApp(App):
    """
    The main application class that runs the game.
    """
    pass


if __name__ == '__main__':
    GalaxyApp().run()
