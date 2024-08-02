'''
UI which allows you to edit the Gcode directly
'''

# At the moment there is no reason to have this. Will keep it anyway.

# The editting features on files do not work as intended

import os.path

from PySide6.QtWidgets import QMainWindow, QTextEdit, QFileDialog

import webbrowser

class EditGcode(QMainWindow):

    # opens the gcode folder
    @staticmethod
    def gcode():
        webbrowser.open("https://stackoverflow.com/questions/68645/class-static-variables-and-methods")

    # opens the path with the entire code
    @staticmethod
    def code():
        print("n")

    def __init__(self,gcode):
        super().__init__()

        self.fileName = gcode

        self.setWindowTitle("GCode Editor[*]")

        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        save_action = file_menu.addAction("Save")
        saveas_action = file_menu.addAction("Save As")
        open_action = file_menu.addAction("Open")
        reset_action = file_menu.addAction("Reset")

        help_menu = menu_bar.addMenu("Help")
        gcode_action = help_menu.addAction("GCode")
        code_action = help_menu.addAction("Code")

        save_action.triggered.connect(self.save_trig)
        saveas_action.triggered.connect(self.saveas_trig)
        open_action.triggered.connect(self.open_trig)
        reset_action.triggered.connect(self.reset)

        gcode_action.triggered.connect(EditGcode.gcode)
        code_action.triggered.connect(EditGcode.code)

        self.editor = QTextEdit()

        if self.fileName:
            self.editor.insertPlainText(open(self.fileName, 'r+').read())
            self.setWindowTitle(str(os.path.basename(self.fileName)) + "[*]")

        self.setCentralWidget(self.editor)

        self.editor.document().modificationChanged.connect(self.setWindowModified)

    #
    def save_trig(self):
        if not self.fileName:
            self.saveas_trig()
        elif self.isWindowModified():
            with open(self.fileName,'w') as f:
                f.write(self.editor.toPlainText())
        else:
            return

    #
    def saveas_trig(self):
        fileName,_ = QFileDialog.getSaveFileName(self, "Save File",
                                 "/home/",
                                 "Text (*.txt);;All files(*.*)")
        
        if fileName:
            with open(fileName, 'w') as f:
                f.write(self.editor.toPlainText())
            self.fileName = fileName
            self.setWindowTitle(str(os.path.basename(fileName)) + "[*]")
           
    # set default opening location to the gcode folder
    def open_trig(self):
        fileName,_ = QFileDialog.getOpenFileName(self, "Open File",
                                                    "/home/",
                                                    "Text (*.txt);;All files(*.*)")
        
        if fileName:
            self.reset()
            with open(fileName, 'r+') as f:
                self.editor.insertPlainText(f.read())
            self.fileName = fileName
            self.setWindowTitle(str(os.path.basename(fileName)) + "[*]")

    # 
    def reset(self):
        self.setWindowTitle("GCode Editor [*]")
        self.editor.setPlainText("")


