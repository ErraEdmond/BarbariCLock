from time import localtime, gmtime, sleep
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from threading import Thread, active_count

import sys 
# while True: 
#     time = localtime()
#     print(f'{time[3]}:{time[4]}')
#     sleep(60)

class MyWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.min = 0
        self.sec = 1
        self.iniUI()


    def iniUI(self): 
        self.setGeometry(500, 200, 600, 600)
        self.setWindowTitle('Brutal Lock')
        # win.setWindowIcon

        self.label = QtWidgets.QLabel(self)
        self.label.setText(f'{self.min} : {self.sec}')
        self.label.setAlignment(Qt.AlignVCenter)

        self.start_button = QPushButton('Push', self)
        self.start_button.clicked.connect(self.ti_thread)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

        self.show()
        self.cl_thread()


    def timer(self):
        while self.isVisible() and self.min >= 0: 
            if self.sec < 0: 
                self.min -= 1
                self.sec = 59
            self.label.setText(f'{self.min}:{str(self.sec).zfill(2)}')
            self.sec -= 1
            sleep(1)


    def clock(self):
        print(active_count())
        while self.isVisible() and active_count() <= 2:
            self.label.setText(f'{localtime()[3]} : {localtime()[4]} : {localtime()[5]}')
            sleep(1)


    def cl_thread(self): 
        t1 = Thread(target=self.clock)
        t1.start()
    
    def ti_thread(self): 
        t1 = Thread(target=self.timer)
        print(active_count())
        t1.start()
        self.cl_thread()
        # looks like I have to find a way to eliminate thread after the end of function.
        # I guess, thread-based solution is temporary. If I would ever create more functionality, I have to add emits 
        # for timer + clock

app = QApplication([])    
win = MyWindow()
win.show()
sys.exit(app.exec_())

