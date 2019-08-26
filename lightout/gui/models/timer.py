from kivy.clock import Clock
from kivy.uix.label import Label

class Timer(Label):
    def __init__(self, **kwargs):
        super(Timer, self).__init__(**kwargs)
        self.time = 0
        self.text = 'Time: 00:00'
    
    def start(self, *args):
        return Clock.schedule_interval(self.update, 1)
    
    def update(self, *args):
        self.time += 1
        self.text = 'Time: {:02d}:{:02d}'.format(self.time//60, self.time%60)
    
    def stop(self, scheduled):
        Clock.unschedule(scheduled)
    
    def reset(self):
        self.time = 0
        self.text = 'Time: 00:00'