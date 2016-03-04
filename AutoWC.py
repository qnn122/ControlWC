#!/usr/bin/env python

"""
Main program
"""

import math
from GetDataSerial import Serial
from WheelchairModel import WheelchairModel

PI = math.pi

class AutoWC:

    def __init__(self):
        # Set up port for incoming data
        self.serial = Serial()

        self.arrayLeftTicks = None
        self.arrayRightTicks = None

        # Wheelchair model
        self.wc = WheelchairModel()

    def sendPackage(self, channel, volt):
        """Send commands to move wheel chair
        :param channel:
        :param volt:
        """
        i = int((volt-1)*80 + 0.5)
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

    def stopWC(self):
        """Stop the wheelchair
        """
        self.sendPackage('a', 2.5)
        self.sendPackage('b', 2.5)

    def updateTicks(self):
        """Update  arrayTicks to print sumTicks to calculate distance
        :returns d_left: distance travelled from left wheel
                 d_right: distance travelled from right wheel
        """
        previous_d_right = self.wc.d_right
        previous_d_left = self.wc.d_left

        self.buffer = self.serial.readPort()  # numbers of ticks of 2 encoders

        LEFT_M_PER_TICK = 2*PI*self.wc.R_left/self.wc.encoder_revolution
        RIGHT_M_PER_TICK = 2*PI*self.wc.R_right/self.wc.encoder_revolution
        for x in range(len(self.buffer)):
            if x % 2 == 0:      # left encoders
                self.arrayLeftTicks += str(ord(self.buffer[x]))+'\n'
                self.wc.d_left += ord(self.buffer[x])*LEFT_M_PER_TICK
            else:               # right encoders
                self.arrayRightTicks += str(ord(self.buffer[x]))+'\n'
                self.wc.d_right += ord(self.buffer[x])*RIGHT_M_PER_TICK

        print 'd_left: %.2f\td_right: %.2f' % (self.wc.d_left, self.wc.d_right)
        return self.wc.d_left, self.wc.d_right


