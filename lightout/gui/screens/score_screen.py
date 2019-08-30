import os

import requests
from firebase import Firebase
import threading
import time


from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar

from gui.models.table_entry import TableEntry


class ScoreScreen(Screen):
    
    def __init__(self, **kwargs):
        super(ScoreScreen, self).__init__(**kwargs)

        self.pressed = None
        self.entries = []
        self.scores = []

        self.build_screen()

    def clear_widgets(self):
        self.remove_widget(self.layout)
        self.layout = None

    def build_screen(self):
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

        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(header)
        self.layout.add_widget(scroll)
        
        self.layout.add_widget(
            Button(text='Back', size_hint_max_y=30, on_press=self.back)
        )

        self.add_widget(self.layout)

        self.pb = ProgressBar(value=0, max=100)
        self.layout.add_widget(self.pb)


    def simulate_loading(self, final_value):
        while self.pb.value != final_value:
            self.pb.value+=1
            time.sleep(0.01)

    def update_scores_with_firebase(self):
        self.pb.value = 0
        config = {
            "apiKey": "AIzaSyAdo9hLvVbA-KI7kwFlx2vOILV_o5K-dBE",
            "authDomain": "pa-project-1-graphs.firebaseapp.com",
            "databaseURL": "https://pa-project-1-graphs.firebaseio.com",
            "storageBucket": ""
        }
        self.simulate_loading(10)
        firebase = Firebase(config)
        self.simulate_loading(20)
        db = firebase.database()
        self.simulate_loading(70)
        player_list = db.child("players").get()
        player_info_list = [player_list.val()[player_key] for player_key in player_list.val()]
        self.simulate_loading(100)
        self.update(player_info_list)
        self.scores = player_info_list

    def on_pre_enter(self):
        if self.layout == None:
            self.build_screen()
        fb_thread = threading.Thread(target=self.update_scores_with_firebase)
        fb_thread.start()

    def on_leave(self):
        self.clear_widgets()
    
    def back(self, btn):
        self.parent.transition.direction = 'left'
        self.parent.current = 'menu'
    
    def update(self, scores):
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

        if btn.text[-1] == u'▴' or btn.text[-1] == u'▾':
            if btn.text[-1] == u'▴':
                btn.text = btn.text[:-1] + u'▾'
                self.sort_descending(int(btn.id))
            
            else:
                btn.text = btn.text[:-1] + u'▴'
                self.sort_ascending(int(btn.id))
        else:
            btn.text = btn.text + u'▾'
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
