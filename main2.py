import sys
import time
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget,
    QPushButton, QHBoxLayout, QMenu, QAction, QComboBox, QMessageBox, QLabel, QFileDialog, QLineEdit, QTextEdit, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import QTimer  # Импорт QTimer

from TECHPTRC import TECHPTRC

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('untitled.ui', self)

        # Найдите нужные элементы интерфейса
        #self.labelOutput = self.findChild(QLabel, 'labelOutput')  # QLabel для отображения выходов
        self.startButton = self.findChild(QPushButton, 'startButton')  # Кнопка старта
        self.stopButton = self.findChild(QPushButton, 'stopButton')  # Кнопка остановки
        self.startButton.clicked.connect(self.start)
        self.stopButton.clicked.connect(self.stop)

        self.ovCheckBox = self.findChild(QCheckBox, 'OV')  # QCheckBox для состояния
        self.VyvodCheckBox = self.findChild(QCheckBox, 'Vyvod')  # QCheckBox для состояния
        self.signCheckBox = self.findChild(QCheckBox, 'sign')  # QCheckBox для состояния
        self.otklkontCheckBox = self.findChild(QCheckBox, 'otklkont')  # QCheckBox для состояния
        self.kiCheckBox = self.findChild(QCheckBox, 'ki')  # QCheckBox для состояния
        self.sbrosCheckBox = self.findChild(QCheckBox, 'sbros')  # QCheckBox для состояния
        self.sgf1CheckBox = self.findChild(QCheckBox, 'sgf1')  # QCheckBox для состояния
        self.sgf2CheckBox = self.findChild(QCheckBox, 'sgf2')  # QCheckBox для состояния

        self.loVvod = self.findChild(QLabel, 'label_9')  # QCheckBox для состояния
        self.loOperVyvod = self.findChild(QLabel, 'label_10')  # QCheckBox для состояния
        self.loSrab = self.findChild(QLabel, 'label_11')  # QCheckBox для состояния
        self.loSrabSign = self.findChild(QLabel, 'label_12')  # QCheckBox для состояния
        self.loZablok = self.findChild(QLabel, 'label_13')  # QCheckBox для состояния

        self.Timer = self.findChild(QLineEdit, 'Timer')  # QCheckBox для состояния
        self.setTime1 = self.findChild(QLineEdit, 'setTimer1')  # QCheckBox для состояния

        self.is_running = False  # Флаг для отслеживания состояния

        # Инициализация таймера
        self.timer = QTimer()
        self.timer.timeout.connect(self.updatePLC)

        # Инициализация TECHPTRC
        #self.ptrc = TECHPTRC(SGF1=0, SGF2=0, T=int(self.setTime1.text()))


    def start(self):
        self.ptrc = TECHPTRC(SGF1=self.sgf1CheckBox.isChecked(), SGF2=self.sgf2CheckBox.isChecked(), T=int(self.setTime1.text()))
        self.is_running = True
        self.timer.start(500)  # Запустите таймер с интервалом 1000 мс (1 секунда)

    def stop(self):
        self.is_running = False
        self.timer.stop()  # Остановите таймер

    def updatePLC(self):
        if not self.is_running:
            return
        # Считываем входы    
        ov_state = self.ovCheckBox.isChecked()
        Vyvod_state = self.VyvodCheckBox.isChecked()
        sign_state = self.signCheckBox.isChecked()
        otklkont_state = self.otklkontCheckBox.isChecked()
        ki_state = self.kiCheckBox.isChecked()
        sbros_state = self.sbrosCheckBox.isChecked()
        sgf1_state = self.sgf1CheckBox.isChecked()
        sgf2_state = self.sgf2CheckBox.isChecked()

        self.ptrc.set_SGF1(sgf1_state)
        self.ptrc.set_SGF2(sgf2_state)
        outputs = self.ptrc.Step(ov_state, Vyvod_state, sign_state, otklkont_state, ki_state, sbros_state)
        # Выставляем выходы
        if outputs[0]:
            self.loVvod.setStyleSheet("background-color: red;")
        else:
            self.loVvod.setStyleSheet("background-color: green;")

        if outputs[1]:
            self.loOperVyvod.setStyleSheet("background-color: red;")
        else:
            self.loOperVyvod.setStyleSheet("background-color: green;")

        if outputs[2]:
            self.loSrab.setStyleSheet("background-color: red;")
        else:
            self.loSrab.setStyleSheet("background-color: green;")

        if outputs[3]:
            self.loSrabSign.setStyleSheet("background-color: red;")
        else:
            self.loSrabSign.setStyleSheet("background-color: green;")

        if outputs[4]:
            self.loZablok.setStyleSheet("background-color: red;")
        else:
            self.loZablok.setStyleSheet("background-color: green;")
        
        self.Timer.setText(str(outputs[5]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())