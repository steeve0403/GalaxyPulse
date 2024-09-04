from kivy.config import Config
from kivy.uix import widget
from kivy.uix.relativelayout import RelativeLayout

from src.effects.audio_manager import AudioManager
from src.effects.visual_manager import VisualManager

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '550')

import random
from kivy.core.window import Window
from kivy import platform
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import Color, Line, Quad, Triangle
from kivy.properties import NumericProperty, Clock, ObjectProperty, StringProperty
from src.utils.constants import *
from src.utils.transforms import transform

Builder.load_file('src/kv_files/menu.kv')


class MainWidget(RelativeLayout):
    from src.utils.user_action import keyboard_closed, on_keyboard_up, on_keyboard_down
    menu_widget = ObjectProperty()

    current_offset_y = 0
    current_y_loop = 0

    current_speed_x = 0
    current_offset_x = 0

    ship = None
    ship_coordinates = [(0, 0), (0, 0), (0, 0)]

    state_game_over = False
    state_game_has_started = False

    menu_title = StringProperty("G A L A X Y")
    menu_button_title = StringProperty("Start")

    score_txt = StringProperty()

    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        # print("Init W:" + str(self.width) + "H:" + str(self.height))
        self.audio_manager = AudioManager()
        self.visual_manager = VisualManager(self)

        self.visual_manager.init_vertical_lines()
        self.visual_manager.init_horizontal_lines()
        self.visual_manager.init_tiles()

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

        self.visual_manager.tiles_coordinates = []
        self.visual_manager.pre_fill_tiles_coordinates()
        self.visual_manager.generate_tiles_coordinates()
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
        for i in range(0, len(self.visual_manager.tiles_coordinates)):
            tile_x, tile_y = self.visual_manager.tiles_coordinates[i]
            if tile_y > self.current_y_loop + 1:
                return False
            if self.check_ship_collision_with_tile(tile_x, tile_y):
                return True
        return False

    def check_ship_collision_with_tile(self, tile_x, tile_y):
        x_min, y_min = self.visual_manager.get_tile_coordinates(tile_x, tile_y)
        x_max, y_max = self.visual_manager.get_tile_coordinates(tile_x + 1, tile_y + 1)
        for i in range(0, 3):
            p_x, p_y = self.ship_coordinates[i]
            if x_min <= p_x <= x_max and y_min <= p_y <= y_max:
                return True
        return False

    def update(self, dt):
        # print("dt : " + str(dt))
        time_factor = dt * 60

        self.visual_manager.update_vertical_lines()
        self.visual_manager.update_horizontal_lines()
        self.visual_manager.update_tiles()
        self.update_ship()

        if not self.state_game_over and self.state_game_has_started:
            speed_y = SPEED * self.height / 100
            self.current_offset_y += speed_y * time_factor

            spacing_y = H_LINES_SPACING * self.height
            while self.current_offset_y >= spacing_y:
                self.current_offset_y -= spacing_y
                self.current_y_loop += 1
                self.score_txt = "Score: " + str(self.current_y_loop)
                self.visual_manager.generate_tiles_coordinates()

            speed_x = self.current_speed_x * self.width / 100
            self.current_offset_x += speed_x * time_factor

        if not self.check_ship_collision() and not self.state_game_over:
            self.state_game_over = True
            self.menu_title = "G A M E  O V E R"
            self.menu_title = "Restart"
            self.menu_widget.opacity = 1
            self.audio_manager.stop_music()
            self.audio_manager.play_music_queue('game_over_impact')
            Clock.schedule_once(self.play_voice_game_over, 3)
            print("GAME OVER")

    def play_voice_game_over(self, dt):
        if self.state_game_over:
            self.audio_manager.play_music_queue('game_over_voice')

    def on_menu_btn_pressed(self):
        if self.state_game_over:
            self.audio_manager.play_music_queue('restart')
        else:
            self.audio_manager.play_music_queue(['begin', 'music1'])
        self.reset_game()
        self.state_game_has_started = True
        self.menu_widget.opacity = 0


class GalaxyApp(App):
    pass


GalaxyApp().run()
