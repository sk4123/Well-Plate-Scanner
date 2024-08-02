'''
Main window for the program
'''

# This Python file uses the following encoding: utf-8

import os.path

from PySide6.QtWidgets import QMainWindow, QFileDialog

# Important:
# You need to run the following command to generate the ui_form.py file
#     pyside6-uic form.ui -o ui_form.py, or
#     pyside2-uic form.ui -o ui_form.py
#
# I found that the created file needs to be copied by hand into the folder, but that's because Qt Creator is annoying

from modules.ui_form import Ui_MainWindow
from modules.editgcode import EditGcode
from modules.portselection import PortSelection
from modules.toarduino import ToArduino
from modules.calibration import Calibration
import webbrowser

class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, app):
        super().__init__()

        # Variables to see if the EditGcode window is active and whether there is any Gcode file loaded
        self.gedit = None
        self.loadedGcode = None

        # Variables for port selection
        self.sel_port = None # holds the portselection instance
        self.port = None

        # Sets the settings to default upon initialization - not yet implemented
        self.fileName = "default"
        self.set_settings(self.fileName)

        # Sets up the UI
        self.setupUi(self)
        self.app = app

        # Code to stop movement - feature not yet implemented
        self.stopcode = ""

        # Variables for selection
        self.mode = None
        self.type = None

        # Variables for speed
        self.feed = [1000,5] # check the speed for z

        # user inputs
        self.x_user = 0
        self.y_user = 0
        self.z_user = 0

        self.x_min_max = [0,80]
        self.y_min_max = [0,100]
        self.z_min_max = [0,40]

        self.calibration = [0,0,0]

        self.y_input.setText(f"{self.y_user}")
        self.z_input.setText(f"{self.z_user}")
        self.x_input.setText(f"{self.x_user}")

        # This is where the ToArduino() instance will live
        self.interpretor = None

        # Buttons and such
        self.actionSave.triggered.connect(self.save)
        self.actionSave_As.triggered.connect(self.saveAs)
        self.actionLoad.triggered.connect(self.load)
        self.actionReset.triggered.connect(self.reset)
        self.actionPorts.triggered.connect(self.ports)
        self.actionGCode.triggered.connect(self.gcode)
        self.actionCode.triggered.connect(self.code)
        self.actionDocumentation.triggered.connect(self.documentation)

        self.actionCalibrate.triggered.connect(self.calibration_mode)

        self.disablemotors.released.connect(self.dismotors)
        self.autohome.released.connect(self.auto_home)

        self.sel_well.toggled.connect(self.well_selection)
        self.sel_row.toggled.connect(self.row_selection)
        self.sel_all.toggled.connect(self.all_selection)

        self.well_edit.returnPressed.connect(self.get_well)
        self.row_edit.returnPressed.connect(self.get_row)
        

        # time - not yet implemented
        self.run.released.connect(self.go)
        self.stop.released.connect(self.stop_running)

        # self.progress_bar

        self.x_home.released.connect(self.x_homed)
        self.y_home.released.connect(self.y_homed)
        self.z_home.released.connect(self.z_homed)

        self.x_input.textChanged.connect(self.x_new_pos)
        self.y_input.textChanged.connect(self.y_new_pos)
        self.z_input.textChanged.connect(self.z_new_pos)

        self.commit.released.connect(self.send)

        self.x_set.released.connect(self.x_home_set)
        self.y_set.released.connect(self.y_home_set)
        self.z_set.released.connect(self.z_home_set)

        self.speed_set.released.connect(self.set_speed)

        self.load_gcode.released.connect(self.loadGcode)
        self.edit_gcode.released.connect(self.editGcode)

        # auto detect serial port
        PortSelection(self).auto_port()

        self.runtime = ToArduino()

        # Calibration
        self.calInst = Calibration()

    #### Menubar functions

    # Saves to the file called "saved", or another file if that is open
    def save(self):
        print("boys")

    # Saves everything to a new file
    def saveAs(self):
        print("Finally")
    
    # Loads a file
    def load(self):
        fileName,_ = QFileDialog.getOpenFileName(self, "Open File",
                                                    "/home/",
                                                    "Text (*.txt);;All files(*.*)")
        
        if fileName:
            self.fileName = str(fileName)
            self.set_settings(fileName)

    # Sets the settings to the active file. INPROGRESS
    def set_settings(self,fileName):
        self.gedit = None
        self.loadedGcode = None

        self.sel_port = None
        self.port = None # add a way to get this port

        self.fileName = "default"

    # Sets everything to the default
    def reset(self):
        self.set_settings(self.fileName)

    # Controls the PortSelection window
    def ports(self):
        if self.sel_port is None:
            self.sel_port = PortSelection(self)
            self.sel_port.show()
        else:
            print("Already up")

    # Controls the calibration window
    def calibration_mode(self):
        if self.port:
            self.calInst.get_port(self.port)
            self.calInst.show()
        else:
            print("No port selected")
    
    # Edit gcode - obsolete
    def gcode(self):
        EditGcode.gcode()
    
    # Edit gcode - obsolete
    def code(self):
        EditGcode.code()

    # Sends you to the repo - change to a google doc with links to Marlin, etc
    def documentation(self):
        webbrowser.open("https://github.com/sk4123/Custom_XY_Stage")



    #### Left hand side

    # Will display that a port is chosen
    def display_port(self):
        print("hello")

    # Will enable/disable the motors
    def dismotors(self):
        print("m")

    # Auto homing feature for all axes
    def auto_home(self):
        self.runtime.change_selection("G28")
        self.runtime.change_port(self.port)
        self.runtime.change_speed(self.feed)
        self.runtime.sendToArduino()

    # Selects the well
    def well_selection(self):
        self.mode = "well"

    # Gets the well
    def get_well(self):
        text = self.well_edit.text().strip().lower()
        # changes these checks
        if len(text) < 4 and int(text[1]):
            self.type = ["well", text]
        else:
            print("Too many characters or an int was not put in")

    # Selects the row
    def row_selection(self):
        self.mode = "row"

    # Gets the row
    def get_row(self):
        text = self.row_edit.text().strip.lower()
        if len(text) < 2 and int(text[0]):
            self.type = ["row", text]
        else:
            print("Too many characters or an int was not put in")

    # Selects everything
    def all_selection(self):
        self.mode = "all"


    # Will show an estimate of how long the operation will take
    def time_est(self):
        print("how")

    # Starts the ToArduino operation
    def go(self):
        # add a check to see if both are non None
        if self.mode == self.type[0]:
            self.runtime.change_selection(self.type)
            self.runtime.change_port(self.port)
            self.runtime.change_speed(self.feed)
            self.runtime.sendToArduino()
        else:
            print("The mode and desired imaging area do not match")

    # Stops everything - not yet implemented, requires an interrupt pin
    def stop_running(self):
        ToArduino(self.port,self.stopcode).sendToArduino()



    #### Center

    # A place for the progress bar
    def setup_progress(self):
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

    # 
    def set_time(self,current_time,max_time):
        self.progress_bar.setValue(100*current_time/max_time)

    #
    def run_bar(self):
        print("something")



    #### Right hand side

    # Tells the Arduino to return to the home position for x
    def x_homed(self):
        ToArduino(self.port,["X",0],self.feed)
    
    # Tells the Arduino to return to the home position for y
    def y_homed(self):
        ToArduino(self.port,["Y",0],self.feed)

    # Tells the Arduino to return to the home position for z
    def z_homed(self):
        ToArduino(self.port,["Z",0],self.feed)

    # a place to read the x
    def x_new_pos(self):
        a = int(self.x_input.text().strip().lower()) + self.calibration[0]
        if (a+1) > self.x_min_max[0] or (a-1) < self.x_min_max[1]:
            self.x_user = self.x_input.text()
        else:
            print("Input exceeds the bounds")

    # a place to read the y
    def y_new_pos(self):
        a = int(self.y_input.text().strip().lower()) + self.calibration[1]
        if (a+1) > self.y_min_max[0] or (a-1) < self.y_min_max[1]:
            self.y_user = self.y_input.text()
        else:
            print("Input exceeds the bounds")

    # a place to read the z
    def z_new_pos(self):
        a = int(self.z_input.text().strip().lower()) + self.calibration[2]
        if (a+1) > self.z_min_max[0] or (a-1) < self.z_min_max[1]:
            self.z_user = self.z_input.text()
        else:
            print("Input exceeds the bounds")

    # A place to read the x and y speeds - I am choosing to combine them
    def get_x_speed(self):
        self.feed[0] = int(self.x_speed.text().strip())

    # a place to read the z speed
    def get_z_speed(self):
        self.feed[1] = int(self.z_speed.text().strip())

    # Shows the gcode edit window
    def editGcode(self):
        if self.gedit is None:
            self.gedit = EditGcode(self.loadedGcode)
            self.gedit.show()

    # Loads in a gcode file
    # Set default to the gcode folders
    def loadGcode(self):
        fileName,_ = QFileDialog.getOpenFileName(self, "Open File",
                                                      "/home/",
                                                      "Text (*.txt);;All files(*.*)")
        if fileName:
            self.loadedGcode = os.path.join(os.path.dirname(os.path.abspath(fileName)),fileName)