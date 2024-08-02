"""
Calibration window
"""


from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout
from modules.toarduino import ToArduino

class Calibration(QWidget):
    calvals = [0,0,0]

    def __init__(self):
        super().__init__()
        
        self.BAUDRATE = 250000

        self.limits_min = [0,0,-40]
        self.limits_max = [100,100,0]

        self.feed = [200,200,30]

        self.setWindowTitle("Calibration")

        x_01 = QPushButton("X+0.1")
        x_1 = QPushButton("X+1")

        xn_01 = QPushButton("X-0.1")
        xn_1 = QPushButton("X-1")

        y_01 = QPushButton("Y+0.1")
        y_1 = QPushButton("Y+1")

        yn_01 = QPushButton("Y-0.1")
        yn_1 = QPushButton("Y-1")

        dip = QPushButton("Test Dip")

        layout = QGridLayout()

        layout.addWidget(x_1,2,4)
        layout.addWidget(x_01,2,3)
        layout.addWidget(dip,2,2)
        layout.addWidget(xn_01,2,1)
        layout.addWidget(xn_1,2,0)

        layout.addWidget(yn_1,4,2)
        layout.addWidget(yn_01,3,2)
        layout.addWidget(y_01,1,2)
        layout.addWidget(y_1,0,2)

        self.setLayout(layout)

        x_01.released.connect(self.press_x_01)
        x_1.released.connect(self.press_x_1)

        xn_01.released.connect(self.press_xn_01)
        xn_1.released.connect(self.press_xn_1)

        y_01.released.connect(self.press_y_01)
        y_1.released.connect(self.press_y_1)

        yn_01.released.connect(self.press_yn_01)
        yn_1.released.connect(self.press_yn_1)

        dip.released.connect(self.press_dip)

        self.dipped = False
        self.last_pos = [0,0,0]

        self.toardu = ToArduino()
        self.port = None

    def get_port(self,v):
        self.port = v

    def check(self,pos,v):
        if Calibration.calvals[pos]+v > self.limits_max[pos] or Calibration.calvals[pos]+v < self.limits_min[pos]:
            print("No")
        else:
            Calibration.calvals[pos] += v
            self.send()

    def press_x_01(self):
        self.file = [0.1,0,0]
        self.check(0,0.1)

    def press_x_1(self):
        self.file = [1,0,0]
        self.check(0,1)


    def press_xn_01(self):
        self.file = [-0.1,0,0]
        self.check(0,-0.1)


    def press_xn_1(self):
        self.file = [-1,0,0]
        self.check(0,-1)


    def press_y_01(self):
        self.file = [0,0.1,0]
        self.check(1,0.1)


    def press_y_1(self):
        self.file = [0,1,0]
        self.check(1,1)


    def press_yn_01(self):
        self.file = [0,-0.1,0]
        self.check(1,-0.1)


    def press_yn_1(self):
        self.file = [0,-1,0]
        self.check(1,-1)

    def press_dip(self):
        if self.dipped:
            self.file = [0,0,20]
        else:
            self.file = [0,0,-20]

        self.check(2,self.file[2])
        self.dipped = not self.dipped

    def send(self,last = None):
        if last:
            self.toardu.change_last = last
        
        self.file.append("G91")

        print(self.file)
        self.toardu.change_selection(self.file)
        self.toardu.change_speed(self.feed)
        self.toardu.change_port(self.port)
        self.toardu.sendToArduino(cal=True)

    def can_exit(self):
        return True

    def closeEvent(self,event):
        if self.can_exit():
            ToArduino.cal = Calibration.calvals[:2]
            event.accept()
        else:
            event.ignore()
