from time import localtime, sleep
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from threading import Thread, active_count 

import sys 

class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.paused = False
        self.stopped = False 
        self.iniUI()

    def iniUI(self): 
        self.setGeometry(500, 200, 600, 600)
        self.setWindowTitle('BarbariCLock: Execute them ALL!')
        self.setWindowIcon(QIcon('icon.png'))

        self.label = QtWidgets.QLabel(self)
        self.label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(lambda: self.ti_thread(tt = True))
        self.pause_button = QPushButton('Pause', self)
        self.pause_button.clicked.connect(lambda: self.regulations(p=True, s=False)) 
        self.stop_button = QPushButton('Stop', self)
        self.stop_button.clicked.connect(lambda: self.regulations(p=False, s=True)) 


        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.pause_button)
        layout.addWidget(self.stop_button)
        self.setLayout(layout)

        self.show()
        self.ti_thread(tt = False)
        self.cl_thread()


    def regulations(self, p : bool, s : bool):
        if p: 
            self.paused = bool(1 - self.paused)
        if s: 
            self.stopped = bool(1 - self.stopped)


    def timer(self, min, sec):
        print(active_count())
        while self.isVisible():
            if min < 0 or self.stopped:
                break
            if sec == 0: 
                min -= 1
                sec = 59

            sleep(1)
            if self.paused == True:
                continue
            self.label.setText(f'{min:02d}:{sec:02d}')
            sec -= 1
        

    def pomadoro(self): 
        self.timer(25, 0)
        self.stopped = False 
        self.timer(5,0)
        self.clock()


    def ti_thread(self, tt : bool):
        th_timer = Thread(target=self.pomadoro)
        if th_timer.is_alive == True: 
            self.timer()
        if tt and th_timer.is_alive != True:
            th_timer.start()
            th_clock.join()


    def clock(self):
        while self.isVisible() and active_count() < 3:
            self.label.setText(f'{localtime()[3]:02d} : {localtime()[4]:02d} : {localtime()[5]:02d}')
            sleep(1)


    def cl_thread (self): 
        global th_clock
        th_clock = Thread(target=self.clock)
        th_clock.start()

app = QApplication([])    
win = MyWindow()
win.show()
sys.exit(app.exec_())

