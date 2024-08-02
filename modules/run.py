from modules.toarduino import ToArduino

class Run():
    def __init__(self,port):
        super().__init__()
        
        self.port = port
        self.file = None
        self.zero_status = None
        self.offset = [0,0]
        

    def zero(self):
        print("use G28 and specify the axes") # do we need P0?

    def calibrate(self):
        # 1. activate calibrate mode (motors on)
        # 2. gcode to middle column
        #initialize offset
        # 3. loop
        # 3.1 give the user the ability to dip (2mm) - make sure this comes up before anything else
        # 3.2. receive small user input (sub 1mm, throw error otherwise)
        # 3.3. move that amount
        # 3.4 if the user is satisfied, end

        self.offset = [offset_x, offset_y]
        print("calibrated")
        

    def get_user_input(self):
        # Negative numbers mean it is inactive
        x = -1
        y = -1
        self.convert_to_coords(x,y)
        self.file = [x,y]

    def convert_to_coords(self,x,y):
        print(f"converted: {x}, {y}")
    
    def calculate_motion(self):
        print("fuck")

    def generate_gcode():
        print("do something")

    def send_code(self):
        # use try and except for the file and port stuff (across the board)
        if self.port and self.file:
            ToArduino(self.port,self.file)
        elif self.port:
            print("The file is not defined.")
        elif self.file:
            print("The port is not defined.")
        else:
            print("Neither the port nor the file are defined.")
