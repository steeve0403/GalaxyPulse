import random

from kivy import platform
from kivy.core.window import Window
from kivy.graphics import Color, Triangle, Quad, Line
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, Clock
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget

from src.effects.audio_manager import AudioManager
from src.utils.constants import *
from src.utils.game_data import GameData
from src.utils.transforms import transform


class MainWidget(Widget):
    from src.utils.transforms import transform
    from src.utils.user_action import keyboard_closed, on_keyboard_up, on_keyboard_down
    menu_screen = ObjectProperty()
    point_perspective_x = NumericProperty(0)
    point_perspective_y = NumericProperty(0)

    # Vertical Lines
    vertical_lines = []

    # Horizontal lines
    horizontal_lines = []

    current_offset_y = 0
    current_y_loop = 0

    current_speed_x = 0
    current_offset_x = 0

    tiles = []
    tiles_coordinates = []

    ship = None
    ship_coordinates = [(0, 0), (0, 0), (0, 0)]

    score_txt = StringProperty()


    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("Init W:" + str(self.width) + "H:" + str(self.height))
        self.audio_manager = AudioManager()
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

        self.audio_manager.play_music_queue(['galaxy', 'music1'])

    def reset_game(self):
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
        if platform in ('linux', 'win', 'macosx'):
            return True
        return False

    def init_ship(self):
        with self.canvas:
            Color(0, 0, 0)
            self.ship = Triangle()

    def update_ship(self):
        center_x = self.width / 2
        base_y = SHIP_BASE_Y * self.height
        half_width = SHIP_WIDTH * self.width / 2
        ship_height = SHIP_HEIGHT * self.height

        #   2
        # 1  3
        self.ship_coordinates[0] = (center_x - half_width, base_y)
        self.ship_coordinates[1] = (center_x, base_y + ship_height)
        self.ship_coordinates[2] = (center_x + half_width, base_y)

        x1, y1 = transform(self, *self.ship_coordinates[0])
        x2, y2 = transform(self, *self.ship_coordinates[1])
        x3, y3 = transform(self, *self.ship_coordinates[2])

        self.ship.points = [x1, y1, x2, y2, x3, y3]

    def check_ship_collision(self):
        tile_range = 2
        for tile_x, tile_y in self.tiles_coordinates:
            if abs(tile_y - self.current_y_loop) > tile_range:
                continue
            if self.check_ship_collision_with_tile(tile_x, tile_y):
                return True
        return False

    def check_ship_collision_with_tile(self, tile_x, tile_y):
        x_min, y_min = self.get_tile_coordinates(tile_x, tile_y)
        x_max, y_max = self.get_tile_coordinates(tile_x + 1, tile_y + 1)
        for i in range(0, 3):
            p_x, p_y = self.ship_coordinates[i]
            if x_min <= p_x <= x_max and y_min <= p_y <= y_max:
                return True
        return False

    def init_tiles(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, NB_TILES):
                self.tiles.append(Quad())

    def pre_fill_tiles_coordinates(self):
        for i in range(0, 10):
            self.tiles_coordinates.append((0, i))

    def generate_tiles_coordinates(self):
        last_y = 0
        last_x = 0

        for i in range(len(self.tiles_coordinates) - 1, -1, -1):
            if self.tiles_coordinates[i][1] < self.current_y_loop:
                del self.tiles_coordinates[i]

        if len(self.tiles_coordinates) > 0:
            last_coordinates = self.tiles_coordinates[-1]
            last_x = last_coordinates[0]
            last_y = last_coordinates[1] + 1

        for i in range(len(self.tiles_coordinates), NB_TILES):
            r = random.randint(0, 2)
            # 0 -> all right
            # 1 -> right
            # 2 -> left
            start_index = -int(V_NB_LINES / 2) + 1
            end_index = start_index + V_NB_LINES - 1
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
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, V_NB_LINES):
                self.vertical_lines.append(Line())

    def get_line_x_from_index(self, index):
        central_line_x = self.point_perspective_x
        spacing = V_LINES_SPACING * self.width
        offset = index - 0.5
        line_x = central_line_x + offset * spacing + self.current_offset_x
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = H_LINES_SPACING * self.height
        line_y = index * spacing_y - self.current_offset_y
        return line_y

    def get_tile_coordinates(self, tile_x, tile_y):
        tile_y = tile_y - self.current_y_loop
        x = self.get_line_x_from_index(tile_x)
        y = self.get_line_y_from_index(tile_y)
        return x, y

    def update_tiles(self):
        for i in range(NB_TILES):
            tile = self.tiles[i]
            tile_coordinates = self.tiles_coordinates[i]
            x_min, y_min = self.get_tile_coordinates(tile_coordinates[0], tile_coordinates[1])
            x_max, y_max = self.get_tile_coordinates(tile_coordinates[0] + 1, tile_coordinates[1] + 1)

            tile.points = [
                *self.transform(x_min, y_min),
                *self.transform(x_min, y_max),
                *self.transform(x_max, y_max),
                *self.transform(x_max, y_min)
            ]

    def update_vertical_lines(self):
        start_index = -int(V_NB_LINES / 2) + 1
        for i in range(start_index, start_index + V_NB_LINES):
            line_x = self.get_line_x_from_index(i)
            x1, y1 = transform(self, line_x, 0)
            x2, y2 = transform(self, line_x, self.height)
            self.vertical_lines[i].points = [x1, y1, x2, y2]

    def init_horizontal_lines(self):
        with self.canvas:
            Color(1, 1, 1)
            for i in range(0, H_NB_LINES):
                self.horizontal_lines.append(Line())

    def update_horizontal_lines(self):
        start_index = -int(V_NB_LINES / 2) + 1
        end_index = start_index + V_NB_LINES - 1

        x_min = self.get_line_x_from_index(start_index)
        x_max = self.get_line_x_from_index(end_index)

        for i in range(0, H_NB_LINES):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = transform(self, x_min, line_y)
            x2, y2 = transform(self, x_max, line_y)
            self.horizontal_lines[i].points = [x1, y1, x2, y2]

    def update(self, dt):
        # print("dt : " + str(dt))
        time_factor = dt * 60

        self.update_vertical_lines()
        self.update_horizontal_lines()
        self.update_tiles()
        self.update_ship()

        if not GameData.state_game_over and GameData.state_game_has_started:
            speed_y = SPEED * self.height / 100
            self.current_offset_y += speed_y * time_factor

            spacing_y = H_LINES_SPACING * self.height
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
            self.ids.menu_screen.opacity = 1
            self.audio_manager.stop_music()
            self.audio_manager.play_music_queue(['gameover_impact'])
            Clock.schedule_once(self.play_voice_game_over, 3)
            print("GAME OVER")

    def play_voice_game_over(self, dt):
        if self.state_game_over:
            self.audio_manager.play_music_queue(['gameover_voice'])




class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game_widget = MainWidget()
        self.add_widget(self.game_widget)
