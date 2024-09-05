from kivy.properties import StringProperty
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen

from src.effects.audio_manager import AudioManager
from src.utils.game_data import GameData


# class MenuApp(RelativeLayout):
#     def on_touch_down(self, touch):
#         if self.opacity == 0:
#             return False
#         return super(RelativeLayout, self).on_touch_down(touch)

class MenuScreen(Screen):
    menu_title = StringProperty("G A L A X Y")
    menu_button_title = StringProperty("Start")
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.audio_manager = AudioManager()  # Initialise l'audio manager

    # def start_game(self):
    #     self.manager.current = 'game_screen'
    #     self.manager.transition.direction = 'left'
    #     print("Start Game")
    #
    # def restart_game(self):
    #     self.manager.get_screen('game_screen').restart_game()
    #     self.manager.current = 'game_screen'
    #     self.manager.transition.direction = 'right'
    #     print("Restart Game")
    #
    # def quit_game(self):
    #     print("Quit Game")
    #     exit()

    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super(RelativeLayout, self).on_touch_down(touch)

    def on_menu_btn_pressed(self):
        if GameData.state_game_over:
            self.audio_manager.play_music_queue('restart')
        else:
            self.audio_manager.play_music_queue(['begin', 'music1'])
        game_screen = self.manager.get_screen('game_screen')
        game_screen.game_widget.reset_game()
        GameData.state_game_has_started = True
        self.ids.menu_screen.opacity = 0
