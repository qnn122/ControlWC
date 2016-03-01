#!/usr/bin/env python

"""
Main program
"""

import numpy as np
from GetDataSerial import Serial
from WheelchairModel import WheelchairModel

class AutoWC:

    def __init__(self):
        self.arrayLeftTicks = None
        self.sumLeftTicks = None
        self.arrayRightTicks = None
        self.sumRightTicks = None

        # Set up port for incoming data
        self.serial = Serial()
        self.port = self.serial.ser

        # Wheelchair model
        self.wc = WheelchairModel()


    def sendPackage(self, channel, volt):
        i = int((volt-1)*80 + 0.5)
        if self.port.isOpen():
            if channel == 'a':
                self.port.write(chr(234))        # 234 is the predefined header
                self.port.write(chr(i))
                print channel + ':  "%.2f"' % volt
            elif channel == 'b':
                self.port.write(chr(i))
                print channel + ':  "%.2f"' % volt
            else:
                print 'The selected channel is unidentified. Cannot send commands'
        else:
            print 'Serial port is not open. Cannot send commands'

    def stopWC(self):
        self.sendPackage('a', 2.5)
        self.sendPackage('b', 2.5)

    def updateTicks(self):
        """Update  arrayTicks to print sumTicks to calculate distance
        :returns d_left: distance travelled from left wheel
                 d_right: distance travelled from right wheel
        """
        previous_d_right = self.wc.d_right
        previous_d_left = self.wc.d_left

        if self.port.inWaiting() > 0:
            buffer = Serial.readPort()  # numbers of ticks of 2 encoders

            LEFT_M_PER_TICK = 2*np.pi*self.wc.R_left/self.wc.encoder_revolution
            RIGHT_M_PER_TICK = 2*np.pi*self.wc.R_right/self.wc.encoder_revolution
            for x in range(0, len(buffer)):
                if x % 2 == 0:      # left encoders
                    self.arrayLeftTicks[x] = str(ord(buffer[x]))
                    # self.sumLeftTicks += ord(buffer[x])
                    self.wc.d_left += ord(buffer[x])*LEFT_M_PER_TICK
                else:               # right encoders
                    self.arrayRightTicks[x] = str(ord(buffer[x]))
                    # self.sumRightTicks += ord(buffer[x])
                    self.wc.d_right += ord(buffer[x])*RIGHT_M_PER_TICK

        print 'd_left: %.2f\td_right: %.2f' % (self.wc.d_left, self.wc.d_right)
        return self.wc.d_left, self.wc.d_right
