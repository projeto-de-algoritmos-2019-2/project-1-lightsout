import os
import pickle

from copy import deepcopy

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Rectangle


from lightout import LightOut

from .blinking import Blinking
from .light import Light
from .moves import Moves
from .timer import Timer

class GameGrid(GridLayout):
    
    def __init__(self, size, difficulty, **kwargs):
        super(GameGrid, self).__init__(**kwargs)

        self._size = size
        self.difficulty = difficulty

        self.game = self.generate_new_game()
        
        self.cols = self.game.size
        self.spacing = self.game.size

        self.moves = Moves()
        self.timer = Timer()

        self.manager = None
        self.scheduled = None
        self.player_name = None
        self.toggled_last = None

        self.best_clicks = []

        with self.canvas.before:
            Color(0.75, 0.75, 0.75, 0.75)
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(pos=self.update_rect, size=self.update_rect)
        self.add_lights()

    def add_lights(self):
        if hasattr(self, 'lights'):
            self.remove_lights()

        self.lights = []
        for cell in self.game.cells:
            
            light = Light(
                is_on=cell.is_on,
                id=str(cell.value),
                on_press=self.toggle
            )

            self.add_widget(light)
            self.lights.append(light)
    
    def remove_lights(self):
        for light in self.lights:
            self.remove_widget(light)
    
    def update_rect(self, instance, value):
        instance.rect.pos = instance.pos
        instance.rect.size = instance.size

    def toggle(self, light):
        id_ = int(light.id)

        self.toggled_last = id_

        self.parent.parent.parent.unsched()

        neighbors_ids = self.game.toggle(position=id_)

        for id_ in neighbors_ids:
            self.lights[id_].flip()

        self.moves.inc()
        self.check_if_completed()
    
    def check_if_completed(self):
        if self.game.is_over():

            self.difficulty += 1
            
            self.timer.stop(self.scheduled)
            current=(self.player_name, self.moves.count, self.timer.text[6:])
            self.manager.new_scores.append(current)

            # todo Save score to a file
            path = os.path.join('static', 'scores')
            with open(path, 'ab') as scores:
                pickle.dump(current, scores)

            options = GridLayout(cols=3)
            
            options.add_widget(Button(text='New Game', 
                font_size=20, 
                on_press=self.new_game)
            )

            options.add_widget(Button(text='Exit', 
                font_size=20, 
                on_press=self.end)
            )

            options.add_widget(Button(text='Back to menu', 
                font_size=20, 
                on_press=self.back)
            )

            self.popup = Popup(
                title = 'Congratulations!',
                title_size = '22',
                title_align='center',
                content=options,
                size_hint=(None, None),
                size=(480, 116),
                auto_dismiss=False
            )

            self.popup.open()

    def new_game(self, btn):
        self.timer.reset()
        self.moves.reset()

        self.generate_new_game()
        self.add_lights()

        self.scheduled = self.timer.start()
        self.popup.dismiss()
    
    def end(self, btn):
        App.get_running_app().stop()
    
    def back(self, btn):
        self.popup.dismiss()
        self.manager.transition.direction = 'right'
        self.manager.current = 'menu'
    
    def generate_new_game(self):
        self.game = LightOut.random_game(self._size, self.difficulty)
        self.original_game = deepcopy(self.game)
        return self.game
    
    def restart(self):
        self.timer.reset()
        self.moves.reset()
        
        self.game = deepcopy(self.original_game)

        self.add_lights()

    def load(self):
        self.timer.reset()
        self.moves.reset()

        for light in self.lights:
            id = int(light.id)
            matching_cell = self.game.cells[id]
            light.initialize(is_on=matching_cell.is_on)
    
    def destroy(self):
        for light in self.lights:
            light.initialize(is_on=False)
    
    def get_next_best_move(self):
        should_recalculate = True

        if len(self.best_clicks) > 0:
            if self.toggled_last == self.best_clicks[0]:
                self.best_clicks = self.best_clicks[1:]
                should_recalculate = False
                print("Used cached hints")

        if should_recalculate:
            self.best_clicks = LightOut.best_cells_to_click(self.game)
            print("Recalculated Game")

        cell_id = self.best_clicks[0]

        # Bug -> Can not find the right path to win the game
        if cell_id is None:
            print(cell_id)
            print("BUG BUG BUG")
            return
        
        return Blinking(
            self.lights[cell_id], 
            Clock.schedule_interval(self.lights[cell_id].blink, 0.5)
        )
