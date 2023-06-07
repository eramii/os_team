from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
import random

class WhacAMoleGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.whacks = 0
        self.hole = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.whac_a_mole)
        
        self.setWindowTitle("Whac-A-Mole")
        self.setStyleSheet("background-color: green;")
        self.setFixedSize(500, 520)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        self.tip_label = QLabel("Play with mouse for best experience", self)
        self.tip_label.setStyleSheet("background-color: black; color: green;")
        self.tip_label.setGeometry(0, 497, 500, 23)

        self.lab_label = QLabel("WHAC-A-MOLE!", self)
        self.lab_label.setFont(QFont("Algerian", 30))
        self.lab_label.setStyleSheet("background-color: blue; color: yellow;")
        self.lab_label.setGeometry(110, 0, 280, 50)

        self.score_label = QLabel(str(self.whacks), self)
        self.score_label.setFont(QFont('Bahnschrift', 30))
        self.score_label.setStyleSheet("background-color: yellow;")
        self.score_label.setGeometry(170, 52, 160, 38)
        self.score_label.move(170, 52)

        self.remark_label = QLabel("", self)
        self.remark_label.setFont(QFont("Centaur", 20))
        self.remark_label.setStyleSheet("background-color: red; color: yellow;")
        self.remark_label.setGeometry(130, 107, 220, 28)

        self.holes=[]
        for i in range(9):
            hole = QPushButton(self)
            hole.setGeometry((i % 3) * 200 + 20, (i // 3) * 130 + 160, 90, 60)
            hole.setStyleSheet("background-color: black;")
            hole.setEnabled(False)
            hole.clicked.connect(lambda checked, hole_num=i+1: self.on_whack(hole_num))
            self.holes.append(hole)
        
        self.show()


    def on_whack(self, hole_num):
        if self.hole == hole_num:
            hole = self.holes[hole_num - 1]
            hole.setEnabled(False)
            hole.setText('_')
            hole.setStyleSheet("background-color: red; color: black;")
            self.whacks += 1
            self.score_label.setText(str(self.whacks))

    def whac_a_mole(self):
        if self.hole != 0:
            hole = self.holes[self.hole - 1]
            hole.setEnabled(False)
            hole.setText('_')
            hole.setStyleSheet("background-color: black;")


        self.hole = random.randint(1, 9)
        hole = self.holes[self.hole - 1]
        hole.setEnabled(True)
        hole.setText('O')
        hole.setStyleSheet("background-color: green; color: black;")

    
    def start_game(self):
        self.whacks = 0
        self.score_label.setText(str(self.whacks))
        self.hole = 0
        self.timer.start(1000)

app = QApplication([])
game = WhacAMoleGame()
game.start_game()
app.exec_()
