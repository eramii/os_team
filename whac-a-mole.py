from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QFont,QPixmap,QIcon
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtMultimedia import QSound  #bgm모듈 추가 Qsound

import random

class WhacAMoleGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.whacks = 0   
        self.hole = 0
        self.fake_hole = 0 #다른 동물이 나올 구멍
        self.mole_icon = QIcon(QPixmap("mole.png")) # 두더지 아이콘
        self.fake_icon = QIcon()                       # 다른 동물 아이콘
        self.fake_images = ["chicken.png", "squid.png", "duck.png"]   # 다른 동물 이미지 경로 리스트
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
        self.lab_label.setFont(QFont("Trebuchet MS", 20))
        self.lab_label.setStyleSheet("background-color: blue; color: yellow;")
        self.lab_label.setGeometry(100, 0, 350, 50)

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
        for i in range(9):          # 비활성화 및 배경 검은색 변경은 disable_hole 함수로 위임
            hole = QPushButton(self)
            hole.setGeometry((i % 3) * 200 + 20, (i // 3) * 130 + 160, 90, 60)
            hole.clicked.connect(lambda checked, hole_num=i+1: self.on_whack(hole_num))
            self.holes.append(hole)

        self.show()

#init 함수에 있던 버튼 비활성화&배경변경 기능 함수
    def disable_hole(self, hole):   # 구멍 비활성화하는 함수
        hole.setEnabled(False)
        hole.setIcon(QIcon())
        hole.setStyleSheet("background-color: red; color: black;")

    def choose_hole(self):          # 두더지와 다른 동물이 나올 위치 선택
        # 두더지가 나올 위치
        self.hole = random.randint(1, 9)
        # 두더지가 나올 위치가 아닌 다른 동물이 나올 위치 선택
        self.fake_hole = random.choice([i for i in range(1, 10) if i != self.hole])
        # fake_hole에 어떤 동물이 나올지 랜덤선택
        fake_img_path = random.choice(self.fake_images)
        self.fake_icon = QIcon(QPixmap(fake_img_path))  # 다른 동물 아이콘 설정


    def on_whack(self, hole_num):
        if hole_num == self.hole:           # 두더지를 잡은 경우:    점수 +1 & 해당 구멍 비활성화
            self.whacks += 1    
        mole_hole = self.holes[self.hole - 1]
        fake_hole = self.holes[self.fake_hole - 1]
        self.disable_hole(mole_hole)
        self.disable_hole(fake_hole)

        self.score_label.setText(str(self.whacks))  # 점수 갱신

    def whac_a_mole(self):          # 두더지 및 다른 동물 등장하는 함수

        self.choose_hole()          # 동물들이 나타날 구멍 고르기

        mole_hole = self.holes[self.hole - 1]
        fake_hole = self.holes[self.fake_hole - 1]
        #나머지 hole들은 비활성화
        for hole in self.holes:
            if hole != mole_hole and hole != fake_hole:
                self.disable_hole(hole)
        # choose_hole()을 통해 설정된 self.hole과 self.fake_hole을 기준으로
        # 두더지와 다른 동물을 나타나게함            
        mole_hole.setEnabled(True)
        mole_hole.setIcon(self.mole_icon)
        mole_hole.setIconSize(mole_hole.size())

        fake_hole.setEnabled(True)
        fake_hole.setIcon(self.fake_icon)
        fake_hole.setIconSize(fake_hole.size())

    
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
