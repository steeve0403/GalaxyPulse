from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
import os

from galaxy import GameScreen
from screens.menu import MenuScreen

kv_folder = os.path.join(os.path.dirname(__file__), 'kv_files')

Builder.load_file(os.path.join(kv_folder, 'galaxy.kv'))
Builder.load_file(os.path.join(kv_folder, 'menu.kv'))

class GalaxyApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu_screen'))
        sm.add_widget(GameScreen(name='game_screen'))
        return sm
