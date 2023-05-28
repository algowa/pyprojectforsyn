import json
import math
import random
import sqlite3
import sys
import time

from PyQt5 import uic, QtGui, QtCore, QtWidgets  # Импортируем uic
from PyQt5.QtMultimedia import QSound, QSoundEffect
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QInputDialog
from windows.FirstGameWindow import FirstGameWindow
from windows.SecondGameWindow import SecondGameWindow
from windows.ProfileWindow import ProfileWindow
from windows.SettingsWindow import SettingsWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uifiles/main.ui', self)  # Загружаем дизайн
        self.con = sqlite3.connect('datebase.db')
        self.cur = self.con.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS 
         multi_table(user_id INTEGER, five_ex INTEGER, ten_ex INTEGER, twenty_ex INTEGER, twentyfive_ex INTEGER,
         fourteen_ex INTEGER, hundred_ex INTEGER)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS 
         sq_table(user_id INTEGER, five_ex INTEGER, ten_ex INTEGER, twenty_ex INTEGER, twentyfive_ex INTEGER,
         fourteen_ex INTEGER)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS 
         users_stats(user_id INTEGER, correct INTEGER, mistakes INTEGER)''')
        self.con.commit()
        try:
            with open('config.json', 'r', encoding='utf-8') as file:
                dic = json.load(file)
                self.user_id = dic['user_id']
        except Exception as e:
            print(e)
            with open('config.json', 'w', encoding='utf-8') as file:
                self.user_id = random.randint(1000000, 9999999)
                self.volume_status = 'on'
                dic = {'user_id': self.user_id,
                       'volume_tik_status': True,
                       'volume_tik_value': 100,
                       'volume_correct_status': True,
                       'volume_correct_value': 100,
                       'volume_mistake_status': True,
                       'volume_mistake_value': 100,
                       'volume_button_status': True,
                       'volume_button_value': 100}
                json.dump(dic, file, indent=4)
                time_to_db = '00:00:00'
                self.cur.execute('INSERT INTO multi_table VALUES(?, ?, ?, ?, ?, ?, ?)',
                                 (self.user_id, time_to_db, time_to_db, time_to_db, time_to_db, time_to_db, time_to_db))
                self.cur.execute('INSERT INTO sq_table VALUES(?, ?, ?, ?, ?, ?)',
                                 (self.user_id, time_to_db, time_to_db, time_to_db, time_to_db, time_to_db))
                self.cur.execute('INSERT INTO users_stats VALUES(?, ?, ?)',
                                 (self.user_id, 0, 0))
                self.con.commit()
        self.cur.close()
        self.setFixedSize(800, 600)
        self.pushButton.clicked.connect(self.show_profile)
        self.pushButton.installEventFilter(self)
        self.pushButton_2.clicked.connect(self.start_game_one)
        self.pushButton_3.clicked.connect(self.start_game_two)
        self.pushButton_5.clicked.connect(self.show_settings)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.game_one = FirstGameWindow(user_id=self.user_id)
        self.game_two = SecondGameWindow(user_id=self.user_id)
        self.settings = SettingsWindow(user_id=self.user_id, main=self)
        self.profile = ProfileWindow(user_id=self.user_id)

        self.button_sound = QSoundEffect()
        sound_filepath = QtCore.QUrl.fromLocalFile("sounds/button.wav")
        self.button_sound.setSource(sound_filepath)

        with open('config.json', 'r', encoding='utf-8') as file:
            self.config_data = json.load(file)
            self.button_sound.setVolume(self.config_data["volume_button_value"] / 100)

    def start_game_one(self):
        self.game_one.show()
        if not(self.settings.isHidden()):
            self.settings.close()
        if self.config_data["volume_button_status"]:
            self.button_sound.play()

    def process_button_sound(self):
        with open('config.json', 'r', encoding='utf-8') as file:
            self.config_data = json.load(file)
            self.button_sound.setVolume(self.config_data["volume_button_value"] / 100)
        if self.config_data["volume_button_status"]:
            self.button_sound.play()

    def update_volume(self):
        with open('config.json', 'r', encoding='utf-8') as file:
            self.config_data = json.load(file)
            self.button_sound.setVolume(self.config_data["volume_button_value"] / 100)

    def start_game_two(self):
        self.game_two.show()
        if not(self.settings.isHidden()):
            self.settings.close()
        if self.config_data["volume_button_status"]:
            self.button_sound.play()
        
    def show_settings(self):
        self.settings.show()
        if not(self.game_one.isHidden()):
            self.game_one.close()
        if not(self.game_two.isHidden()):
            self.game_two.close()
        if self.config_data["volume_button_status"]:
            self.button_sound.play()

    def show_profile(self):
        self.profile.show()
        if self.config_data["volume_button_status"]:
            self.button_sound.play()

    def closeEvent(self, event):
        pass