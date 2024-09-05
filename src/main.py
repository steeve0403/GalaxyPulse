import cProfile

from kivy.config import Config

from src.app import GalaxyApp

Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '550')




GalaxyApp().run()

if __name__ == '__main__':
    cProfile.run('run_app()', sort='time')
