
from kivy.uix.label import Label


class TableEntry:
    def __init__(self, cols):
        self.name  = Label(text=str(cols[0]),      font_size=25, height=20)
        self.moves = Label(text=str(cols[1]), font_size=25, height=20)
        self.time  = Label(text=str(cols[2]),      font_size=25, height=20)
