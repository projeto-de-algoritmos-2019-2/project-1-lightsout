import os

from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from game_grid import GameGrid
    
class GameScreen(Screen):

    def __init__(self, size, difficulty=1, **kwargs):
        super(GameScreen, self).__init__(**kwargs)

        self.blinking = None
        self.pressed = False

        self.game_grid = GameGrid (
            size = size, 
            difficulty = difficulty,
            size_hint_min_y = 620
        )

        header = BoxLayout(orientation='horizontal')
        header.add_widget(self.game_grid.timer)
        header.add_widget(self.game_grid.moves)

        box = BoxLayout(orientation='vertical')
        box.add_widget(header)
        box.add_widget(self.game_grid)

        footer = BoxLayout(orientation='horizontal', size_hint_max_y=40)
        footer.add_widget(Button(text='Hint', on_press=self.hint))
        footer.add_widget(Button(text='Restart', on_press=self.restart))
        footer.add_widget(Button(text='Menu', on_press=self.back))

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(box)
        layout.add_widget(footer)

        self.add_widget(layout)
    
    # def on_pre_enter(self):
    #     self.game_grid.load()
    
    def on_enter(self):
        self.game_grid.scheduled = self.game_grid.timer.start()
    
    def back(self, btn):
        self.parent.transition.direction = 'right'
        self.parent.current = 'menu'

    def hint(self, btn):
        if self.blinking is None:
            self.blinking = self.game_grid.get_next_best_move()
    
    def unsched(self):
        if self.blinking is not None:
            Clock.unschedule(self.blinking.scheduled)
            self.blinking.button.restore()
            self.blinking = None
    
    def restart(self, btn):
        self.game_grid.timer.stop(self.game_grid.scheduled)
        self.game_grid.scheduled = self.game_grid.timer.start()
        self.game_grid.restart()
        
        if self.blinking:
            self.unsched()
        