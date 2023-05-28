import json
import math
import random
import sqlite3
import sys
import time

from PyQt5 import uic, QtGui, QtCore, QtWidgets
from PyQt5.QtMultimedia import QSound, QSoundEffect
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QInputDialog


class ProfileWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        uic.loadUi('uifiles/profile.ui', self)
        self.user_id = user_id
        self.setFixedSize(800, 600)
        self.comboBox.activated[str].connect(self.onChangedFirst)
        self.comboBox_2.activated[str].connect(self.onChangedSecond)

        self.button_sound = QSoundEffect()
        sound_filepath = QtCore.QUrl.fromLocalFile("sounds/button.wav")
        self.button_sound.setSource(sound_filepath)
        with open('config.json', 'r', encoding='utf-8') as file:
            self.config_data = json.load(file)
            self.button_sound.setVolume(self.config_data["volume_button_value"] / 100)

    def showEvent(self, event):
        with open('config.json', 'r', encoding='utf-8') as file:
            self.config_data = json.load(file)
            self.button_sound.setVolume(self.config_data["volume_button_value"] / 100)
        nums = {'5': 'five_ex', '10': 'ten_ex', '20': 'twenty_ex',
                '25': 'twentyfive_ex', '40': 'fourteen_ex',
                '100': 'hundred_ex'}
        get_first_box = self.comboBox.currentText()
        get_second_box = self.comboBox_2.currentText()
        con = sqlite3.connect('datebase.db')
        cur = con.cursor()
        get_score = [i[0] for i in cur.execute(f'SELECT {str(nums[get_first_box])} FROM multi_table WHERE user_id = {self.user_id}')]
        get_score_2 = [i[0] for i in cur.execute(f'SELECT {str(nums[get_second_box])} FROM sq_table WHERE user_id = {self.user_id}')]
        get_all_correct = [i[0] for i in cur.execute(f'SELECT correct FROM users_stats WHERE user_id = {self.user_id}')]
        get_all_mistakes = [i[0] for i in cur.execute(f'SELECT mistakes FROM users_stats WHERE user_id = {self.user_id}')]
        cur.close()
        self.label_3.setText(str(get_score[0]))
        self.label_5.setText(str(get_score_2[0]))
        if get_all_mistakes[0] != 0:
            get_correct_mistakes = float('{:.2f}'.format(get_all_correct[0] / get_all_mistakes[0]))
        else:
            get_correct_mistakes = float('{:.2f}'.format(get_all_correct[0]))
        self.label_9.setText(str(get_all_correct[0]))
        self.label_8.setText(str(get_all_mistakes[0]))
        self.label_11.setText(str(get_correct_mistakes))

    def onChangedFirst(self, text):
        nums = {'5': 'five_ex', '10': 'ten_ex', '20': 'twenty_ex',
                '25': 'twentyfive_ex', '40': 'fourteen_ex',
                '100': 'hundred_ex'}
        con = sqlite3.connect('datebase.db')
        cur = con.cursor()
        get_score = [i[0] for i in cur.execute(f'SELECT {nums[text]} FROM multi_table WHERE user_id = {self.user_id}')]
        cur.close()
        self.label_3.setText(str(get_score[0]))
        if self.config_data["volume_button_status"]:
            self.button_sound.play()

    def onChangedSecond(self, text):
        nums = {'5': 'five_ex', '10': 'ten_ex', '20': 'twenty_ex',
                '25': 'twentyfive_ex', '40': 'fourteen_ex',
                '100': 'hundred_ex'}
        con = sqlite3.connect('datebase.db')
        cur = con.cursor()
        get_score_2 = [i[0] for i in cur.execute(f'SELECT {nums[text]} FROM sq_table WHERE user_id = {self.user_id}')]
        cur.close()
        self.label_5.setText(str(get_score_2[0]))
        if self.config_data["volume_button_status"]:
            self.button_sound.play()