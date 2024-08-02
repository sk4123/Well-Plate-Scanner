'''
Simple UI to select the port through which the device communicates with the Arduino

Not needed if only one Arduino is plugged in
'''

import serial.tools.list_ports as list_ports

from PySide6.QtWidgets import QWidget, QLineEdit, QListWidget, QVBoxLayout

class PortSelection(QWidget):

    def __init__(self,master):
        super().__init__()

        self.master = master
        
        self.setWindowTitle("Arduino Serial Port Selection")

        v_layout = QVBoxLayout()

        self.label = QListWidget()
        self.label.addItems(self.get_ardus())

        self.type = QLineEdit("Type the port, exactly as shown, here")
        self.type.returnPressed.connect(self.selection)

        v_layout.addWidget(self.label)
        v_layout.addWidget(self.type)

        self.setLayout(v_layout)

    # how do i make this update automatically? something with list_ports.comports() i think
    def get_ardus(self):
        return [a.device for a in list_ports.comports() if 'Arduino' in a.description]
    
    #
    def selection(self):
        self.master.port = self.type.text()

    def auto_port(self):
        if len(list_ports.comports()) == 0:
            print("No available devices")
        elif len(list_ports.comports()) == 1:
            self.master.port = list_ports.comports()[0].name
            print(f"The new port is {self.master.port}")
        else:
            print("Too many ports, please go to the port UI to decide.")
        
