#!/usr/bin/env python

"""
Main program
"""

import math
from GetDataSerial import Serial
from WheelchairModel import WheelchairModel

PI = math.pi


class AutoWC:
    """Interface between mainProgram (GUI) and serial port
    Send information from the program to serial port and vice versa
    """
    def __init__(self):
        # Set up port for incoming data
        self.serial = Serial()

        # Buffer for latest data
        self.buffer = 0

    def send_package(self, channel, volt):
        """Send commands to move wheel chair
        :param channel:
        :param volt:
        """
        i = int((volt - 1) * 80 + 0.5)
        try:
            if self.serial.ser.isOpen():
                if channel == 'a':
                    self.serial.ser.write(chr(234))        # 234 is the predefined header
                    self.serial.ser.write(chr(i))
                    print channel + ':  "%.2f"' % volt
                elif channel == 'b':
                    self.serial.ser.write(chr(i))
                    print channel + ':  "%.2f"' % volt
                else:
                    print 'The selected channel is unidentified. Cannot send commands'
        except AttributeError:
            print 'Serial port is not open. Cannot send commands'

    def update_buffer(self):
        """Get latest data stored in serial port's buffer
        """
        self.buffer = self.serial.read_port()  # numbers of ticks of 2 encoders

    def stop_wc(self):
        """Stop the wheelchair
        """
        self.send_package('a', 2.5)
        self.send_package('b', 2.5)



