#!/usr/bin/env python

"""
Communicate with serial port
"""

import serial
import time

class Serial:

    def __init__(self):
        self.ser = None
        self.buffer = None

    def openPort(self, COM):
        self.ser = serial.Serial(port="COM"+COM,
                                 baudrate=19200,
                                 bytesize=serial.EIGHTBITS,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE,
                                 timeout=1)
        print(self.ser.name)
        time.sleep(2)                   # Give time for microcontroller to prepare
        self.ser.flush()                # flush all data from memory
        hello = self.ser.read(100)      # read all data from memory (if any)
        print hello

    def closePort(self):
        if hasattr(self, 'ser'):
            if self.ser.isOpen():
                self.ser.close()
        else:
            print "Serial port has never been created. Terminate the program."


    def readPort(self):
        """
        Read buffer from serial port
        :return: buffer
        """
        self.buffer = self.ser.read(self.ser.inWaiting())
        return self.buffer
    