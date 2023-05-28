import math
import random
import sqlite3
import sys
import time

from PyQt5 import uic, QtGui, QtCore, QtWidgets  # Импортируем uic
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QPushButton, QInputDialog
from windows.MainWindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())