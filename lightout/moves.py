from kivy.uix.label import Label

class Moves(Label):
    def __init__(self, **kwargs):
        super(Moves, self).__init__(**kwargs)
        self.count = 0
        self.text = 'Moves: 0'
    
    def inc(self):
        self.count += 1
        self.text = f'Moves: {self.count}'
    
    def dec(self):
        self.count -= 1
        self.text = f'Moves: {self.count}'
    
    def reset(self):
        self.count = 0
        self.text = 'Moves: 0'