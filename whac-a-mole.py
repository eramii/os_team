from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtMultimedia import QSound  #bgm모듈 추가
import random

class WhacAMoleGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.whacks = 0   
        self.hole = 0
        self.remaining_num=30
        self.timer = QTimer()
        #일정한 시간간격마다 self.whac_a_mole 호출
        #self.timer.timeout.connect(self.whac_a_mole) ->뒤에서 connect가 겹쳐서 뒤에 추가함 
        
        self.setWindowTitle("김지수교수님의 추첨게임")  #창의 제목
        self.setStyleSheet("background-color: green;")#위젯 스타일
        self.setFixedSize(500, 550) #창크기 고정
        self.setWindowFlags(Qt.WindowStaysOnTopHint)#해당 창을 항상 다른 창 위에 표시
        
        #텍스트 표시
        self.tip_label = QLabel("Play with mouse for best experience", self)
        self.tip_label.setStyleSheet("background-color: black; color: green;")
        self.tip_label.setGeometry(0, 497, 500, 23) #위젯 위치,크기

        self.lab_label = QLabel("당첨의 주인공은 누구?!", self)
        self.lab_label.setFont(QFont("Trebuchet MS", 30))
        self.lab_label.setStyleSheet("background-color: blue; color: yellow;")
        self.lab_label.setGeometry(110, 0, 280, 50)

        self.score_label = QLabel(str(self.whacks), self)
        self.score_label.setFont(QFont('Bahnschrift', 30))
        self.score_label.setStyleSheet("background-color: yellow;")
        self.score_label.setGeometry(170, 52, 160, 38)
        self.score_label.move(170, 52) # 위젯 위치 이동

        self.remark_label = QLabel("", self)
        self.remark_label.setFont(QFont("Centaur", 20))
        self.remark_label.setStyleSheet("background-color: red; color: yellow;")
        self.remark_label.setGeometry(130, 107, 220, 28)

        self.time_label = QLabel(str(self.remaining_num),self)
        self.remark_label.setFont(QFont("Centaur", 20))
        self.remark_label.setStyleSheet("background-color: red; color: yellow;")
        self.remark_label.setGeometry(100, 107, 220, 28)


        self.holes=[]
        for i in range(9):
            hole = QPushButton(self)
            hole.setGeometry((i % 3) * 200 + 20, (i // 3) * 130 + 160, 90, 60)
            hole.setStyleSheet("background-color: black;")
            hole.setEnabled(False)  #비활성화 상태
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
        #첫번째 이후
        if self.hole != 0:
            hole = self.holes[self.hole - 1]
            hole.setEnabled(False)
            hole.setText('_')
            hole.setStyleSheet("background-color: black;")

        #게임 시작하고 나서 처음 두더지
        self.hole = random.randint(1, 9)
        hole = self.holes[self.hole - 1]
        hole.setEnabled(True)
        hole.setText('O')  #두더지 부분
        hole.setStyleSheet("background-color: green; color: black;") #두더지부분

    
    def start_game(self):
        self.whacks = 0
        self.score_label.setText(str(self.whacks))
        self.hole = 0
        self.remaining_num= 30  # 두더지 나오는 수
        self.timer_interval = 1000  #단위: 밀리초(1000밀리초 = 1초)

        
        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_event)
        self.timer.start(self.timer_interval)
        self.bgm = QSound("C:/Users/wjg/Downloads/mole_bgm.wav") #bgm 설정
        self.bgm.play()


    
    def timer_event(self):
        self.remaining_num -= 1
        
        if self.remaining_num >= 0:
            self.time_label.setText(str(self.remaining_num))   # 남은 횟수 업데이트
            self.whac_a_mole()
            if self.remaining_num < 10:  #10초남으면 속도 두배
                self.timer_interval =500
                self.timer.setInterval(self.timer_interval)
        else:
            # 시간 종료 시 게임 오버 처리
            self.game_over()   #구현안된거같아서

    def game_over(self):       #구현함
        self.timer.stop()  # 타이머 정지
        self.bgm.stop()  # BGM 정지
    
        # 게임 종료 메시지 박스 표시
        message = "게임 종료!\n총 점수: {}".format(self.whacks)
        QMessageBox.information(self, "게임 종료", message)
    


    



app = QApplication([])
game = WhacAMoleGame()
game.start_game()
app.exec_()
