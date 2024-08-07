README for DM320T (older model, worked)

View as a raw file for best performance

Running main.py will run the program.

Current design features:
    Capable of moving to individual wells (to check)
    Capable of moving along specified rows (to check)
    Calibration


Necessary changes:
    Moving to all wells (iterated row movement)
    Integration with optics (possible timer, or a command from the computer)
        Includes the dipping, part of making the system function
    Adding the option to input your own gcode commands directly
    Remove the "Edit gcode" feature
    Make the progress bar work
    Add a signal indicating the arduino is connected
    New stepper drivers
    Add errors
    Styling
    Making the UI better match the program requirements


This currently runs on Python 12.4 through a virtual environment, but was mostly developed in Python 11.5.
Libraries include:
    PySide6 version 6.7.2
    Pyserial version 3.5
Anything greater than or equal to these should work.

This uses Marlin 3d printer firmware: https://marlinfw.org/

The folder named "Marlin" contains the Marlin 2.1.2.4 code used on the Arduino Mega: https://github.com/MarlinFirmware. The main change files are Marlin/Configuration.h, Marlin/Configuration_adv.h, and Marlin/src/pins/mega/pins_MEGACONTROLLER.h. These files will replace those in Marlin 2.1.2.4. Full changes are below:
    Configuration.h
        91: BOARD_MEGACONTROLLER
        162-164: TB6560
        176: Commented
        231: 0
        552: 0
        560: 0
        652-654: Commented
        876-879: Commented
        1199: { 400, 400, 63*4 }
        1206: { 1000, 1000, 100 }
        1305: Commented
        1637-1639: 1
        1640: Commented
        1671: true
        1725: 80
        1726: 100
        1734: 40
    Configuration_adv.h
        1103: { false, false, false }
        3102: Uncommented -> for tmc only
    pins_MEGACONTROLLER.h
        50-55: 37, 38, 40, 41, 42, 43
        67-77: 2, 3, 22, 4, 5, 23, 6, 7, 24
        79-81: 58, 59, 60
        91 & 93: 61
        97 & 99: 62
        102: 63
        105 & 107: 64
These changes are then uploaded to the board using Arduino IDE or VSCode (with the Arduino extension and some light setup)
        
How Marlin communication works:
    Basically, you send gcode strings from the computer to the board running Marlin over serial. See modules/toarduino.py for more information. Marlin interprets these commands. Why should you use Marlin instead of sending serial commands? It allows for easier reproducibility, less work in the long run (you don't have to hand code every position), allows for relative and absolute motion, etc. Marlin turns the device into a 3d printer without the printing.
    Ex: If you want to move at max speed to position X=2mm, you send "G0 X2" (Marlin defaults to Absolute Positions).
    Commands: https://marlinfw.org/meta/gcode/