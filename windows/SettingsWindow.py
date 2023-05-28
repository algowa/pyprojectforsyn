import json
import math
import random
import sqlite3
import sys
import time

from PyQt5 import uic, QtGui, QtCore, QtWidgets 
from PyQt5.QtMultimedia import QSound, QSoundEffect
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QInputDialog


class SettingsWindow(QMainWindow):
    def __init__(self, user_id, main):
        super().__init__()
        uic.loadUi('uifiles/settings.ui', self)
        self.user_id = user_id
        self.main_window = main
        self.setFixedSize(800, 600)
        self.horizontalSlider.valueChanged[int].connect(self.valuechange)
        self.horizontalSlider_2.valueChanged[int].connect(self.valuechange2)
        self.horizontalSlider_3.valueChanged[int].connect(self.valuechange3)
        self.horizontalSlider_4.valueChanged[int].connect(self.valuechange4)
        self.comboBox.activated[str].connect(self.onChangedFirst)
        self.comboBox_2.activated[str].connect(self.onChangedSecond)
        self.comboBox_3.activated[str].connect(self.onChangedThird)
        self.comboBox_4.activated[str].connect(self.onChangedFourth)

        self.button_sound = QSoundEffect()
        sound_filepath = QtCore.QUrl.fromLocalFile("sounds/button.wav")
        self.button_sound.setSource(sound_filepath)
        with open('config.json', 'r', encoding='utf-8') as file:
            self.config_data = json.load(file)
            self.button_sound.setVolume(self.config_data["volume_button_value"] / 100)

    def onChangedFirst(self, value):
        obj = "volume_tik_status"
        self.change_volume_status(obj, value)

    def onChangedSecond(self, value):
        obj = "volume_correct_status"
        self.change_volume_status(obj, value)

    def onChangedThird(self, value):
        obj = "volume_mistake_status"
        self.change_volume_status(obj, value)

    def onChangedFourth(self, value):
        obj = "volume_button_status"
        self.change_volume_status(obj, value)

    def change_volume_status(self, obj, value):
        try:
            with open('config.json', 'r', encoding='utf-8') as file:
                dic = json.load(file)
                dic[obj] = True if value == 'on' else False
            with open('config.json', 'w', encoding='utf-8') as file:
                json.dump(dic, file, indent=4)
        except Exception:
            pass

    def valuechange(self, value):
        obj = 'volume_tik_value'
        self.changeVolumeValue(obj=obj, value=value)

    def valuechange2(self, value):
        obj = 'volume_correct_value'
        self.changeVolumeValue(obj=obj, value=value)

    def valuechange3(self, value):
        obj = 'volume_mistake_value'
        self.changeVolumeValue(obj=obj, value=value)

    def valuechange4(self, value):
        obj = 'volume_button_value'
        self.changeVolumeValue(obj=obj, value=value)

    def changeVolumeValue(self, obj, value):
        try:
            with open('config.json', 'r', encoding='utf-8') as file:
                dic = json.load(file)
                dic[obj] = value
            with open('config.json', 'w', encoding='utf-8') as file:
                json.dump(dic, file, indent=4)
        except Exception:
            pass

    def showEvent(self, event):
        with open('config.json', 'r', encoding='utf-8') as file:
            dic = json.load(file)
            try:
                self.comboBox.setCurrentIndex(0 if dic["volume_tik_status"] else 1)
                self.comboBox_2.setCurrentIndex(0 if dic["volume_correct_status"] else 1)
                self.comboBox_3.setCurrentIndex(0 if dic["volume_mistake_status"] else 1)
                self.comboBox_4.setCurrentIndex(0 if dic["volume_button_status"] else 1)
                self.horizontalSlider.setValue(dic["volume_tik_value"])
                self.horizontalSlider_2.setValue(dic["volume_correct_value"])
                self.horizontalSlider_3.setValue(dic["volume_mistake_value"])
                self.horizontalSlider_4.setValue(dic["volume_button_value"])
            except Exception as e:
                print(e)

    def update_volume(self):
        with open('config.json', 'r', encoding='utf-8') as file:
            self.config_data = json.load(file)
            self.button_sound.setVolume(self.config_data["volume_button_value"] / 100)

    def closeEvent(self, event):
        self.main_window.update_volume()