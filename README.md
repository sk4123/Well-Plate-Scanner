Running main.py will run the program.

Current design features:
    Capable of moving to individual wells (to check)
    Capable of moving along specified rows (to check)
    Calibration


Necessary changes:
    Moving to all wells (iterated row movement)
    Integration with optics (possible timer, or a command from the computer)
        Includes the dipping, part of making the system function
    Remove (or tweak) the "Edit gcode" feature
    Make the progress bar work
    Add a signal indicating the arduino is connected
    New stepper drivers
    Add errors
    Styling
    Making the UI better match the program requirements

    Lengthen the endstop wires
    Make a board for the new drivers
    Get the new drivers to work (link the links!)
    Make a doc for all the links
    New microstep is 8 - change the steps/rev!
    Find a way to get SpreadCycle / StallGuard on the drivers (acts as its own endstop) ??
    Create a terminal which allows you to input commands and allows Marlin to speak back


This currently runs on Python 12.4 through a virtual environment.
Libraries include:
    PySide6 version 6.7.2
    Pyserial version 3.5
Anything greater than or equal to these should work.

The folder named "ui" contains the files used to create the UI using the open-source version of QT Creator: https://www.qt.io/download-open-source. It is available on another repo. QT Creator is a pain to work with.

The folder named "Marlin" contains the Marlin 2.1.2.4 code used on the Arduino Mega: https://github.com/MarlinFirmware. The main change files are Marlin/Configuration.h, Marlin/Configuration_adv.h, and Marlin/src/pins/mega/pins_MEGACONTROLLER.h. These files will replace those in Marlin 2.1.2.4. Full changes are below:
    Configuration.h
        91: BOARD_MEGACONTROLLER
        162-164: TMC2209
        176: Commented
        231: 0
        552: 0
        560: 0
        652-654: Commented
        876-879: Commented
        1199: { 400, 400, 63*4 } - dependent on microsteps! currently set for 2
        1206: { 1000, 1000, 100 }
        1219: Removed the last number
        1305: Commented
        1637-1639: TESTING THE DEFAULT FOR TMC2209
        1640: Commented
        1671: true
        1725: 80
        1726: 100
        1734: 40
        3258: Uncomment
    Configuration_adv.h
        1103: { false, false, false }
        2734: 1400
        2736: 8
        2754: 1400
        2756: 8
        2998: Uncommented
        2999: Uncommented, 1
        3000: Uncommented, 2
        3065: 24V
        3102: Uncommented
    pins_MEGACONTROLLER
        50-55: 37, 38, 40, 41, 42, 43
        67-77: 65, 66, 22, 67, 68, 23, 69, 70, 24
        79-81: 58, 59, 60
        87-121: 
            #if HAS_TMC_UART//HAS_DRIVER(TMC2209)
            /**
            * TMC2209 stepper drivers
            *
            * Hardware serial communication ports.
            * If undefined software serial is used according to the pins below
            */
            //#define X_HARDWARE_SERIAL  Serial1
            //#define X2_HARDWARE_SERIAL Serial1
            //#define Y_HARDWARE_SERIAL  Serial1
            //#define Y2_HARDWARE_SERIAL Serial1
            //#define Z_HARDWARE_SERIAL  Serial1
            //#define Z2_HARDWARE_SERIAL Serial1
            //#define E0_HARDWARE_SERIAL Serial1
            //#define E1_HARDWARE_SERIAL Serial1
            //#define E2_HARDWARE_SERIAL Serial1
            //#define E3_HARDWARE_SERIAL Serial1
            //#define E4_HARDWARE_SERIAL Serial1

            //
            // Software serial
            //

            #define X_SERIAL_TX_PIN    4
            #define X_SERIAL_RX_PIN    2

            #define Y_SERIAL_TX_PIN    4
            #define Y_SERIAL_RX_PIN    2

            #define Z_SERIAL_TX_PIN    4
            #define Z_SERIAL_RX_PIN    2

            #define TMC_BAUD_RATE 19200

            #endif
        127 & 129: 61
        133 & 135: 62
        138: 63
        141 & 143: 64

    
    Setting the drivers:
        Need to install the TMC2209 library

        For the steppers, rotate the potentiometer clockwise (when looking from the bottom) until the lip faces the bottom
        

