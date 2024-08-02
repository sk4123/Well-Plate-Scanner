"""
Calibration window
"""


from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout
from modules.toarduino import ToArduino

class Calibration(QWidget):

    # Calibration values should not reinitialize whenever a new object is created
    # Z included just in case, no current support added
    calvals = [0,0,0]

    def __init__(self):
        super().__init__()
        
        # Same baudrate as Marlin
        self.BAUDRATE = 250000

        # Setting software limits. These are consistent with Marlin
        # Changed from -40 to +40. The effect on check is unclear
        self.limits_min = [0,0,40]
        self.limits_max = [80,100,0]

        # Setting calibration feed rates
        self.feed = [200,200,30]

        self.setWindowTitle("Calibration")

        # Creating a simple UI for the calibration
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

        # Adding function to the buttons in the UI being released
        x_01.released.connect(self.press_x_01)
        x_1.released.connect(self.press_x_1)

        xn_01.released.connect(self.press_xn_01)
        xn_1.released.connect(self.press_xn_1)

        y_01.released.connect(self.press_y_01)
        y_1.released.connect(self.press_y_1)

        yn_01.released.connect(self.press_yn_01)
        yn_1.released.connect(self.press_yn_1)

        dip.released.connect(self.press_dip)

        # Keeps track of whether or not the Z stage is dipped and where we were
        self.dipped = False
        self.last_pos = [0,0,0]

        # Instantiating a ToArduino class so that commands can be sent smoothly
        self.toardu = ToArduino()
        self.port = None

    # Calibration port set on initialization
    def get_port(self,v):
        self.port = v

    # Checks if the next position will violate the software endstops
    def check(self,pos,v):
        if Calibration.calvals[pos]+v > self.limits_max[pos] or Calibration.calvals[pos]+v < self.limits_min[pos]:
            print("No")
        else:
            Calibration.calvals[pos] += v
            self.send()

    # Moves 0.1mm in the x direction
    def press_x_01(self):
        self.file = [0.1,0,0]
        self.check(0,0.1)

    # Moves 1mm in the x direction
    def press_x_1(self):
        self.file = [1,0,0]
        self.check(0,1)

    # Moves -0.1mm in the x direction
    def press_xn_01(self):
        self.file = [-0.1,0,0]
        self.check(0,-0.1)

    # Moves -1mm in the x direction
    def press_xn_1(self):
        self.file = [-1,0,0]
        self.check(0,-1)

    # Moves 0.1mm in the y direction
    def press_y_01(self):
        self.file = [0,0.1,0]
        self.check(1,0.1)

    # Moves 1mm in the y direction
    def press_y_1(self):
        self.file = [0,1,0]
        self.check(1,1)

    # Moves -0.1mm in the y direction
    def press_yn_01(self):
        self.file = [0,-0.1,0]
        self.check(1,-0.1)

    # Moves -1mm in the y direction
    def press_yn_1(self):
        self.file = [0,-1,0]
        self.check(1,-1)

    # Moves the z actuator by 20mm
    def press_dip(self):
        if self.dipped:
            self.file = [0,0,20]
        else:
            self.file = [0,0,-20]

        self.check(2,self.file[2])
        self.dipped = not self.dipped

    # Sends the gcode
    def send(self,last = None):
        if last:
            self.toardu.change_last = last
        
        # Ensures relative motion
        self.file.append("G91")

        print(self.file)
        self.toardu.change_selection(self.file)
        self.toardu.change_speed(self.feed)
        self.toardu.change_port(self.port)
        self.toardu.sendToArduino(cal=True)

    # Checks to see if the window can close - always true for now
    def can_exit(self):
        return True

    # On window closing, the calibration values are sent to ToArduino()
    def closeEvent(self,event):
        if self.can_exit():
            ToArduino.cal = Calibration.calvals[:2]
            event.accept()
        else:
            event.ignore()
