import os
import pickle


from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView

from table_entry import TableEntry

class ScoreScreen(Screen):
    
    def __init__(self, **kwargs):
        super(ScoreScreen, self).__init__(**kwargs)

        self.pressed = None
        self.entries = []
        self.scores = []
    
        font = os.path.join('static', 'FreeSans.ttf')

        self.names = Button(
            text= u'Names',
            font_name = font,
            font_size='30',
            on_press=self.sort,
            id='0'
        )

        self.moves = Button(
            text= u'Moves',
            font_name = font,
            font_size='30',
            on_press=self.sort,
            id='1'
        )

        self.time = Button(
            text= u'Time',
            font_name = font,
            font_size='30',
            on_press=self.sort,
            id='2'
        )

        header = GridLayout(cols=3, size_hint_max_y=50)
        header.add_widget(self.names)
        header.add_widget(self.moves)
        header.add_widget(self.time)

        scroll = ScrollView(size_hint=(1, None), size=(750, 610))
        self.table = GridLayout(cols=3, size_hint_max_y=None)
        scroll.add_widget(self.table)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(header)
        layout.add_widget(scroll)
        
        layout.add_widget(
            Button(text='Back', size_hint_max_y=30, on_press=self.back)
        )

        self.add_widget(layout)

        try:
            with open(os.path.join('static', 'scores'), 'rb') as scores:
                while True:
                    try:
                        self.scores.append(pickle.load(scores))
                    
                    except EOFError:
                        break
        except IOError:
            pass
        
        if self.scores:
            self.update(self.scores)

        self.sort(self.names)
    

    def on_pre_enter(self):
        self.scores.extend(self.parent.new_scores)
        self.update(self.parent.new_scores)

        self.sort_ascending(0)
        self.rearrange()
        self.parent.new_scores = []
    
    def back(self, btn):
        self.parent.transition.direction = 'left'
        self.parent.current = 'menu'
    
    def update(self, scores):
        if self.scores:

            entries = [TableEntry(score) for score in scores]

            self.entries.extend(entries)
            
            for entry in entries:
                self.table.add_widget(entry.name)
                self.table.add_widget(entry.moves)
                self.table.add_widget(entry.time)
                self.table.height += 3 * 20
            
    def rearrange(self):
        for entry, score in zip(self.entries, self.scores):
            entry.name.text = score[0]
            entry.moves.text = str(score[1])
            entry.time.text = score[2]
    
    def sort(self, btn):
        if btn.text[-1] == u'▴':
            btn.text = btn.text[:-1] + u'▾'
            self.sort_descending(int(btn.id))
        
        else:
            btn.text = btn.text[:-1] + u'▴'
            self.sort_ascending(int(btn.id))
        
        self.rearrange()

        if self.pressed != btn:
            if self.pressed:
                self.pressed.text = self.pressed.text[:-1]
            self.pressed = btn
    
    def sort_ascending(self, key):
        self.scores = sorted(self.scores, key=lambda x: x[key])
    
    def sort_descending(self, key):
        self.scores = sorted(self.scores, reverse=True, key=lambda x: x[key])
