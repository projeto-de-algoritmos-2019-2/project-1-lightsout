import os

from kivy.uix.button import Button

class Light(Button):

    DOWN = os.path.join('static', 'down.png')
    NORMAL = os.path.join('static', 'up.png')
    HINT = os.path.join('static', 'hint.png')

    def __init__(self, is_on, **kwargs):
        super(Light, self).__init__(**kwargs)
        self.toggled = 0
        self.always_release = True
        self.initialize(is_on)
    
    def initialize(self, is_on):
        if is_on:
            self.toggled = 1
            self.background_down = Light.DOWN
            self.background_normal = Light.NORMAL
        
        else:
            self.toggled = 0
            self.background_down = Light.NORMAL
            self.background_normal = Light.DOWN
    
    def on_release(self):
        self.flip()
    
    def flip(self):
        self.toggled = 0 if self.toggled else 1
        self.background_normal, self.background_down = \
            self.background_down, self.background_normal

    def blink(self, *args):
        if self.toggled:
            if self.background_normal == Light.HINT:
                self.background_normal = Light.NORMAL
            else:
                self.background_normal = Light.HINT
        else:
            if self.background_normal == Light.HINT:
                self.background_normal = Light.DOWN
            else:
                self.background_normal = Light.HINT
    
    def restore(self):
        if self.toggled:
            self.background_normal = Light.NORMAL
        else:
            self.background_normal = Light.DOWN