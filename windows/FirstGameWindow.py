import json
import math
import random
import sqlite3
import sys
import time

from PyQt5 import uic, QtGui, QtCore, QtWidgets
from PyQt5.QtMultimedia import QSound, QSoundEffect
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QInputDialog
from windows.SettingsWindow import SettingsWindow


class FirstGameWindow(QMainWindow):
    def __init__(self, user_id):
        super().__init__()
        uic.loadUi('uifiles/second.ui', self)
        self.user_id = user_id
        self.setFixedSize(800, 600)
        self.pushButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_3.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_7.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_8.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_9.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_10.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_11.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_12.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_13.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.pushButton.clicked.connect(self.enter_number)
        self.pushButton_2.clicked.connect(self.enter_number)
        self.pushButton_3.clicked.connect(self.enter_number)
        self.pushButton_7.clicked.connect(self.enter_number)
        self.pushButton_8.clicked.connect(self.enter_number)
        self.pushButton_9.clicked.connect(self.enter_number)
        self.pushButton_10.clicked.connect(self.enter_number)
        self.pushButton_11.clicked.connect(self.enter_number)
        self.pushButton_12.clicked.connect(self.enter_number)
        self.pushButton_13.clicked.connect(self.enter_number)

        self.pushButton_15.clicked.connect(self.del_number)
        self.pushButton_14.clicked.connect(self.clear_number)

        self.pushButton_14.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_15.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_16.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        self.isStartedTimer = False
        self.counterEx = 0
        self.counterTask = 0
        self.startTime = 0

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerProcess)

        self.pushButton_21.clicked.connect(self.start_timer)
        self.pushButton_22.clicked.connect(self.stop_timer)
        self.pushButton_16.clicked.connect(self.ok_button)

        self.pushButton_21.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_22.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_7.setReadOnly(True)
        self.lineEdit_8.setReadOnly(True)

        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_4.setReadOnly(True)
        self.lineEdit_5.setReadOnly(True)
        self.lineEdit_6.setReadOnly(True)

        self.lineEdit_2.setVisible(False)
        self.lineEdit_7.setVisible(False)
        self.lineEdit_8.setVisible(False)

        self.correct_sound = QSoundEffect()
        sound_filepath = QtCore.QUrl.fromLocalFile("sounds/correct.wav")
        self.correct_sound.setSource(sound_filepath)

        self.button_sound = QSoundEffect()
        sound_filepath = QtCore.QUrl.fromLocalFile("sounds/button.wav")
        self.button_sound.setSource(sound_filepath)

        self.incorrect_sound = QSoundEffect()
        sound_filepath = QtCore.QUrl.fromLocalFile("sounds/incorrect.wav")
        self.incorrect_sound.setSource(sound_filepath)

        self.tik_sound = QSoundEffect()
        sound_filepath = QtCore.QUrl.fromLocalFile("sounds/tik.wav")
        self.tik_sound.setSource(sound_filepath)
        self.tik_sound.setLoopCount(QSoundEffect.Infinite)

        with open('config.json', 'r', encoding='utf-8') as file:
            self.config_data = json.load(file)
            self.tik_sound.setVolume(self.config_data["volume_tik_value"] / 100)
            self.incorrect_sound.setVolume(self.config_data["volume_mistake_value"] / 100)
            self.correct_sound.setVolume(self.config_data["volume_correct_value"] / 100)
            self.button_sound.setVolume(self.config_data["volume_button_value"] / 100)

    def ok_button(self):
        if self.isStartedTimer:
            self.counterEx += 1
            if self.lineEdit.text() != '' and self.lineEdit.text().isdigit():
                num0, num1 = map(int, [self.lineEdit_3.text(), self.lineEdit_5.text()])
                result = int(self.lineEdit.text())
                if num0 * num1 == result:
                    self.process_correct_answer()
                elif num0 * num1 != result:
                    self.process_wrong_answer()
                if self.counterEx == self.counterTask:
                    self.timer.stop()
                    self.show_end_dialog()
                else:
                    self.gen_numbers()
            else:
                # print(f'{self.counterEx} - {self.counterTask}')
                self.process_wrong_answer()
                if self.counterEx == self.counterTask:
                    self.timer.stop()
                    self.show_end_dialog()
                else:
                    self.gen_numbers()

    def process_correct_answer(self):
        get_correct = int(self.lineEdit_7.text().split(': ')[1])
        self.lineEdit_7.setText(f'correct: {get_correct + 1}')
        con = sqlite3.connect('datebase.db')
        cur = con.cursor()
        get_all_correct = [i[0] for i in cur.execute(f'SELECT correct FROM users_stats WHERE user_id = {self.user_id}')]
        cur.execute(f'UPDATE users_stats SET correct = {get_all_correct[0] + 1} WHERE user_id = {self.user_id}')
        con.commit()
        cur.close()
        if self.config_data["volume_correct_status"]:
            self.correct_sound.play()

    def process_wrong_answer(self):
        get_mistakes = int(self.lineEdit_8.text().split(': ')[1])
        self.lineEdit_8.setText(f'mistakes: {get_mistakes + 1}')
        con = sqlite3.connect('datebase.db')
        cur = con.cursor()
        get_all_mistakes = [i[0] for i in
                            cur.execute(f'SELECT mistakes FROM users_stats WHERE user_id = {self.user_id}')]
        cur.execute(f'UPDATE users_stats SET mistakes = {get_all_mistakes[0] + 1} WHERE user_id = {self.user_id}')
        con.commit()
        cur.close()
        if self.config_data["volume_mistake_status"]:
            self.incorrect_sound.play()

    def show_end_dialog(self):
        dlg = QDialog()
        uic.loadUi('uifiles/end_game_dialog.ui', dlg)
        dlg.setFixedSize(400, 300)
        correct = self.lineEdit_7.text()
        mistakes = self.lineEdit_8.text()
        dlg.label_2.setText(correct)
        dlg.label_3.setText(mistakes)
        target_time = float('{:.2f}'.format(time.time() - self.startTime))
        if int(mistakes.split(': ')[1]) == 0:
            nums = {'5': 'five_ex', '10': 'ten_ex', '20': 'twenty_ex',
                    '25': 'twentyfive_ex', '40': 'fourteen_ex',
                    '100': 'hundred_ex'}
            con = sqlite3.connect('datebase.db')
            cur = con.cursor()
            get_score = [i[0] for i in cur.execute(f'SELECT {nums[str(self.counterTask)]} FROM multi_table WHERE user_id = {self.user_id}')]
            score = list(map(int, get_score[0].split(':')))
            milisec = score[0] * 60 * 1000 + score[1] * 1000 + score[2]
            target_score_t = f'{int(target_time // 60):02}:{int(target_time % 60):02}:{int(str(target_time).split(".")[1]):02}'
            target_score = list(map(int, target_score_t.split(':')))
            milisec2 = target_score[0] * 60 * 1000 + target_score[1] * 1000 + target_score[2]
            if milisec2 < milisec or milisec == 0:
                cur.execute(f'UPDATE multi_table SET {nums[str(self.counterTask)]} = "{target_score_t}" WHERE user_id = {self.user_id}')
                con.commit()
            cur.close()
        output_time = f'Время: {int(target_time // 60):02}:{int(target_time % 60):02}:{int(str(target_time).split(".")[1])}'
        dlg.label_4.setText(output_time)
        self.stop_timer()
        dlg.exec_()

    def gen_numbers(self):
        num0, num1 = map(str, [random.randint(1, 9), random.randint(1, 9)])
        self.lineEdit.setText('')
        self.lineEdit_3.setText(num0)
        self.lineEdit_5.setText(num1)

    def start_timer(self):
        if self.config_data["volume_button_status"]:
            self.button_sound.play()
        self.stop_timer()
        # dlg = QInputDialog.setComboBoxItems(['5', '10', '20', '25', '40', '100'])
        count, ok_pressed = QInputDialog.getItem(self, "Выберите количество примеров", "Количество примеров", ('5', '10', '20', '25', '40', '100'), 1, False)
        if ok_pressed:
            self.isStartedTimer = True
            self.counterTask = int(count)
            self.gen_numbers()
            self.startTime = time.time()
            self.lineEdit_2.setVisible(True)
            self.lineEdit_7.setVisible(True)
            self.lineEdit_8.setVisible(True)
            self.timer.start(20)
            if self.config_data['volume_tik_status']:
                self.tik_sound.play()

    def stop_timer(self):
        if self.config_data["volume_button_status"]:
            self.button_sound.play()
        self.counterTask = 0
        self.counterEx = 0
        self.isStartedTimer = False
        self.startTime = 0
        self.lineEdit_2.setVisible(False)
        self.lineEdit_7.setVisible(False)
        self.lineEdit_8.setVisible(False)
        self.lineEdit_3.setText('0')
        self.lineEdit_5.setText('0')
        self.lineEdit.setText('0')
        self.lineEdit_2.setText('00:00:00')
        self.lineEdit_7.setText('correct: 0')
        self.lineEdit_8.setText('mistakes: 0')
        try:
            self.timer.stop()
            self.tik_sound.stop()
        except Exception:
            pass

    def timerProcess(self):
        if self.isStartedTimer:
            target_time = float('{:.2f}'.format(time.time() - self.startTime))
            output_time = f'{int(target_time // 60):02}:{int(target_time % 60):02}:{int(str(target_time).split(".")[1]):02}'
            self.lineEdit_2.setText(output_time)

    def exit(self):
        if self.config_data["volume_button_status"]:
            self.button_sound.play()
        self.isStartedTimer = False
        self.lineEdit.setText('0')
        self.close()

    def enter_number(self):
        if self.config_data["volume_button_status"]:
            self.button_sound.play()
        text = self.lineEdit.text()
        if len(text) < 4:
            target_number = self.sender().text()
            text += target_number
            self.lineEdit.setText(text)

    def del_number(self):
        if self.config_data["volume_button_status"]:
            self.button_sound.play()
        text = self.lineEdit.text()
        if len(text) != 0:
            text = text[:len(text) - 1]
            self.lineEdit.setText(text)

    def clear_number(self):
        if self.config_data["volume_button_status"]:
            self.button_sound.play()
        self.lineEdit.setText('')

    def show_error_dialog(self, error: str):
        dlg = QDialog()
        uic.loadUi('uifiles/error_dialog.ui', dlg)
        dlg.setFixedSize(400, 300)
        dlg.label.setText(f'Error:\n{error}')
        dlg.exec_()

    def showEvent(self, event):
        with open('config.json', 'r', encoding='utf-8') as file:
            self.config_data = json.load(file)
            self.tik_sound.setVolume(self.config_data["volume_tik_value"] / 100)
            self.incorrect_sound.setVolume(self.config_data["volume_mistake_value"] / 100)
            self.correct_sound.setVolume(self.config_data["volume_correct_value"] / 100)
            self.button_sound.setVolume(self.config_data["volume_button_value"] / 100)

    def closeEvent(self, event):
        self.counterTask = 0
        self.counterEx = 0
        self.isStartedTimer = False
        self.startTime = 0
        self.lineEdit_2.setVisible(False)
        self.lineEdit_7.setVisible(False)
        self.lineEdit_8.setVisible(False)
        self.lineEdit_3.setText('0')
        self.lineEdit_5.setText('0')
        self.lineEdit.setText('0')
        self.lineEdit_2.setText('00:00:00')
        self.lineEdit_7.setText('correct: 0')
        self.lineEdit_8.setText('mistakes: 0')
        try:
            self.timer.stop()
            self.tik_sound.stop()
        except Exception:
            pass