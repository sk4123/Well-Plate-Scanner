'''
Class which handles data transfer between the computer and the Arduino (through Gcode)

This class handles everything about sending
'''

import serial
import time
import sys

class ToArduino():

    last_coord = [0,0,0]
    cal = [0,0,0]

    def __init__(self):
        super().__init__()

        self.port = None
        self.BAUDRATE = 250000
        self.zero_status = None
        self.selection = None
        self.coords = [0,0,0]
        self.initCoords = [0,0,0]
        self.speed = [0,0]
        self.dwell = 9
        self.speed = None
        
        self.file = None
        self.last_queue = []

        self.predip = 0
        self.dip = 20

    def get_port(self):
        return self.port

    def change_port(self,v):
        self.port = v

    def get_selection(self):
        return self.selection
    
    def change_selection(self,v):
        self.selection = v

    def get_speed(self):
        return self.speed
    
    def change_speed(self,v):
        self.speed = v

    def get_last(self):
        return self.last_coord
    
    def change_last(self,v):
        self.last_coord = v

    def zero(self):
        print("use G28 and specify the axes") # do we need P0?

    def convert_user_input(self):
        if self.selection[0] == "well":
            col = int(self.selection[1][1:len(self.selection[0])-1])
            self.initCoords = [self.row(self.selection[1][0]), col]
            self.convert_well_to_coords()
        elif self.selection[0] == "row":
            col = int(self.selection[1][0:len(self.selection[0])-1])
            self.initCoords = [0, col]
            self.convert_row_to_coords()
        elif self.selection[0] == "all":
            rows = [i for i in range(1,9)]
            cols = [i for i in range(1,13)]
            self.initCoords = [rows,cols]
        else:
            print("Invalid Input")

    # setting zero to be the middle of H1
    def row(self, let:str):
        switch={
            "a":0,
            "b":1,
            "c":2,
            "d":3,
            "e":4,
            "f":5,
            "g":6,
            "h":7
        }
        return switch.get(let,"Invalid Input")

    def convert_well_to_coords(self):
        arr = self.initCoords
        x = arr[0]
        y = arr[1]
        x , y = x*self.dwell, (12-y)*self.dwell
        self.coords = [x,y]
        self.generate_gcode()

    def convert_row_to_coords(self):
        coords=[]
        col = self.initCoords[1]
        y = (12-col)*self.dwell
        for i in range(8):
            x = i*self.dwell
            coords.append([x,y])
        self.coords = coords
        self.generate_gcode(single=False)

    def generate_gcode(self,single=True):
        '''
        "# open a file
        my_file = open('myfile.txt', 'w')
        # get some info
        print('Name: ', my_file.name)
        print('Is Closed : ', my_file.closed)
        print('Opening Mode: ', my_file.mode)
        # write to file
        my_file.write('I love Python')
        my_file.write(' and JavaScript')
        my_file.close()
        # append to file
        my_file = open('myfile.txt', 'a')
        my_file.write(' I also like PHP')
        my_file.close()
        # read from file
        my_file = open('myfile.txt', 'r+')
        text = my_file.read(100)
        print(text)
        '''
        if single:
            x = self.coords[0] + ToArduino.cal[0]
            y = self.coords[1] + ToArduino.cal[1]

            # make this add things on better
            if self.speed:
                final1 = [f"G1 F{self.speed[0]} X{x} Y{y}", f"G1 F{self.speed[1]} Z{self.dip}"]
                final2 = [f"F1 F{self.speed[1]} Z{self.predip}"]

                if len(self.selection) == 4:
                    final1 = [self.selection[3]]
                else:
                    final1 = ["G90",
                                f"G92 X{ToArduino.last_coord[0]} Y{ToArduino.last_coord[1]} Z{ToArduino.last_coord[2]}"]
                
                self.file.append(final1)
                if final2:
                    self.file.append(final2)
            else:
                self.file = f"G0 X{x} Y{y}"

        else:
            for i in range(len(self.coords)):
                x = self.coords[i][0] + ToArduino.cal[0]
                y = self.coords[i][1] + ToArduino.cal[1]

                # make this add things on better
                if self.speed:
                    final1 = [f"G1 F{self.speed[0]} X{x} Y{y}", f"G1 F{self.speed[1]} Z{self.dip}"]
                    final2 = [f"G1 F{self.speed[1]} Z{self.predip}"]
                else:
                    final1 = [f"G0 X{x} Y{y}", f"G0 Z{self.dip}"]
                    final2 = [f"G0 Z{self.predip}"]

                self.file.append(final1)
                self.file.append(final2)

    def get_file(self):
        if self.selection[0] != "G":
            try:
                self.coords = [float(self.selection[0]),float(self.selection[1]),float(self.selection[2])]
            except:
                self.convert_user_input()
        else:
            self.file = [self.selection]

    def manual(self):
        if self.selection[0] == "X":
            self.file = f"G1 F1000 X{self.selection[1]}"
            self.sendToArduino()
        elif self.selection[0] == "Y":
            self.file = f"G1 F1000 Y{self.selection[1]}"
            self.sendToArduino()
        elif self.selection[0] == "Z":
            self.file = f"G1 F1000 Z{self.selection[1]}"
            self.sendToArduino()
        else:
            print("Error")

    # Credits to ShyBoy233 and the code PyGcodeSender for the serial code
    def sendToArduino(self, cal=False):
        # Works but there's a delay
        # use try and except

        print(f"Calibration: {ToArduino.cal}")
        
        self.get_file()

        if self.port and self.file:
            try: 
                ser = serial.Serial(self.port,self.BAUDRATE,timeout=2)
            except:
                print("Nope")
                sys.exit()
            
            ser.write(b"\r\n\r\n")
            time.sleep(1)
            ser.reset_input_buffer()

            if cal:
                print(self.file)
                for code in self.file:
                    ser.write((code+'\n').encode())
            else:

                for code in self.file:
                    code = code.strip()
                    semi = code[1:].find(';')
                    if semi > -1:
                        code = code[:semi]
                    if code.startswith(';') or code.isspace() or len(code) <= 0:
                        continue
                    else:
                        ser.write((code+'\n').encode())

                    xpos = code.find('X')
                    ypos = code.find('Y')
                    zpos = code.find('Z')

                    print(f"Xpos: {xpos} | Ypos: {ypos} | Zpos: {zpos}")

                    if xpos > 0:
                        ToArduino.last_coord[0] = code[xpos+1:].strip()
                    elif ypos > 0:
                        ToArduino.last_coord[1] = code[ypos+1:].strip()
                    elif zpos > 0:
                        ToArduino.last_coord[2] = code[zpos+1:].strip()

                    print(f"Last coords: {ToArduino.last_coord}")

                    # for some reason Marlin isn't sending anything back
                    '''
                        while(1):
                            if ser.readline().startswith(b'ok'):
                                break
                        '''

                # implement some delay function?
                print(f"Port Selection: {self.port} | Command Sent: {self.file}")
                
                self.last_queue = self.file
                self.file = None
        else:
            print("Error")
            print(f"Port Selection: {self.port} | File Name: {self.file}")
