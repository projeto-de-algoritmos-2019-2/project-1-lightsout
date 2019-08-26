import os
from kivy.config import Config

Config.set('graphics', 'resizable', 'false')
Config.set('graphics', 'width', '750')
Config.set('graphics', 'height', '700')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from game_screen import GameScreen
from menu_screen import MenuScreen
from score_screen import ScoreScreen

class Manager(ScreenManager):

    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.game = None
        self.new_scores = []

class LightsOut(App):
    def build(self):
        self.title = 'Lights Out'
        self.icon = os.path.join('static', 'bulb.ico')

        sm = Manager()
        game_screen = GameScreen(name='game', size=5, difficulty=1)
        game_screen.game_grid.manager = sm
        sm.game = game_screen.game_grid

        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(game_screen)
        sm.add_widget(ScoreScreen(name='score'))

        return sm

if __name__ == '__main__':
    LightsOut().run()