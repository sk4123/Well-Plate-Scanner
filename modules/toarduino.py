'''
Class which handles data transfer between the computer and the Arduino (through Gcode)
'''

import serial
import time
import sys

class ToArduino():

    # The last place and the calibration should not change with instantiation
    last_coord = [0,0,0]
    cal = [0,0,0]

    def __init__(self):
        super().__init__()

        # Creating sending variables
        self.port = None
        self.BAUDRATE = 250000
        self.speed = None

        # Creating checking variable
        self.zero_status = None

        # Initializes place for user input
        self.selection = None

        # Initializes place for the sent file
        self.file = None

        # Creating coordinate variables
        self.coords = [0,0,0]
        self.initCoords = [0,0,0]

        # The width, in mm, on the well
        self.dwell = 9

        # Houses the last command sent - not used for anything atm 
        self.last_queue = []

        # Some idea for Z dipping, old and unused
        self.predip = 0
        self.dip = 20

    # Returns the connected port
    def get_port(self):
        return self.port

    # Changes the connected port
    def change_port(self,v):
        self.port = v

    # Returns the current desired motion
    def get_selection(self):
        return self.selection
    
    # Changes the desired motion
    def change_selection(self,v):
        self.selection = v

    # Returns the feed rate
    def get_speed(self):
        return self.speed
    
    # Changes the feed rate
    def change_speed(self,v):
        self.speed = v

    # Returns the last coordinated
    def get_last(self):
        return self.last_coord
    
    # Changes the last coordinate - only for emergencies
    def change_last(self,v):
        self.last_coord = v

    # Converts user input to a more manageable form - used with well, row, and all selection
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

    # setting zero to be the middle of H1 - outputs the rows in numerical form
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

    # Converts a well to coordinates
    def convert_well_to_coords(self):
        arr = self.initCoords
        x = arr[0]
        y = arr[1]
        x , y = x*self.dwell, (12-y)*self.dwell
        self.coords = [x,y]
        self.generate_gcode()

    # Converts a row to coordinates
    def convert_row_to_coords(self):
        coords=[]
        col = self.initCoords[1]
        y = (12-col)*self.dwell
        for i in range(8):
            x = i*self.dwell
            coords.append([x,y])
        self.coords = coords
        self.generate_gcode(single=False)

    # Generates gcode - definitely needs to be improved, one of the most important functions
    # Should be split into multiple functions
    def generate_gcode(self,single=True):
        # Single means that one request is sent
        if single:
            x = self.coords[0] + ToArduino.cal[0]
            y = self.coords[1] + ToArduino.cal[1]

            # Starting to implement Z dipping with motions - relies on communcation with optics, timings need to be set
            if self.speed:
                final1 = [f"G1 F{self.speed[0]} X{x} Y{y}", f"G1 F{self.speed[1]} Z{self.dip}"]
                final2 = [f"F1 F{self.speed[1]} Z{self.predip}"]

                # 
                if len(self.selection) == 4:
                    final1 = [self.selection[3]]
                else:
                    final1 = ["G90",
                                f"G92 X{ToArduino.last_coord[0]} Y{ToArduino.last_coord[1]} Z{ToArduino.last_coord[2]}"]
                
                self.file.append(final1)
                if final2:
                    self.file.append(final2)
            else:
                # Fast move to the x and y positions. Need to check dip status
                self.file = f"G0 X{x} Y{y}"

        else:
            # This is starter code for multiple commands being sent. Again, the z code needs to change
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

    # Determines whether or not the selection needs to be converted or not
    def get_file(self):
        if self.selection[0] != "G":
            try:
                self.coords = [float(self.selection[0]),float(self.selection[1]),float(self.selection[2])]
            except:
                self.convert_user_input()
        else:
            self.file = [self.selection]

    # Takes input for manual motion
    # Should make the feedrate be changed externally
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
    # Sends the code to Arduino
    def sendToArduino(self, cal=False):
        # There is a delay between hitting send and the code sending which is not present with ShyBoy233

        print(f"Calibration: {ToArduino.cal}")
        
        self.get_file()

        if self.port and self.file:
            try: 
                ser = serial.Serial(self.port,self.BAUDRATE,timeout=2)
            except:
                print("Nope")
                sys.exit()
            
            # Waking up the microcontroller
            ser.write(b"\r\n\r\n")
            time.sleep(1)
            ser.reset_input_buffer()

            # If in calibration mode
            if cal:
                print(self.file)
                for code in self.file:
                    ser.write((code+'\n').encode())
            
            # If not in calibration mode
            else:

                for code in self.file:
                    # Removes anything which isn't text
                    code = code.strip()
                    semi = code[1:].find(';')

                    # Ignores semicolons and lines with semicolons
                    if semi > -1:
                        code = code[:semi]
                    if code.startswith(';') or code.isspace() or len(code) <= 0:
                        continue
                    else:
                        # Sends
                        ser.write((code+'\n').encode())

                    # Finds the X, Y, and Z values. Relies on them all being sent in separate lines
                    xpos = code.find('X')
                    ypos = code.find('Y')
                    zpos = code.find('Z')

                    print(f"Xpos: {xpos} | Ypos: {ypos} | Zpos: {zpos}")

                    # Sets the last position to the values sent - -1 implies nothing is found, and nothing goes below 0
                    # >= would work too, but since something "G" comes first, it is not needed
                    if xpos > 0:
                        ToArduino.last_coord[0] = code[xpos+1:].strip()
                    elif ypos > 0:
                        ToArduino.last_coord[1] = code[ypos+1:].strip()
                    elif zpos > 0:
                        ToArduino.last_coord[2] = code[zpos+1:].strip()

                    print(f"Last coords: {ToArduino.last_coord}")

                    # For some reason Marlin isn't sending anything back
                    # Needs to be investiaged. Possibly set up the LCD?
                    '''
                    while(1):
                        if ser.readline().startswith(b'ok'):
                            break
                        '''
                print(f"Port Selection: {self.port} | Command Sent: {self.file}")
                
                # Resets the function
                self.last_queue = self.file
                self.file = None
        else:
            print("Error")
            print(f"Port Selection: {self.port} | File Name: {self.file}")
