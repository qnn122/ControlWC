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

        global LEFT_M_PER_TICK, RIGHT_M_PER_TICK
        LEFT_M_PER_TICK = 2*PI*self.wc.R_left/self.wc.encoder_revolution
        RIGHT_M_PER_TICK = 2*PI*self.wc.R_right/self.wc.encoder_revolution

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

    def update_buffer(self):
        """Update buffer
        """
        self.buffer = self.serial.readPort()  # numbers of ticks of 2 encoders

    def get_distance(self):
        """Get TOTAL distance travelled
        :return:
        """
        for x in range(len(self.buffer)):
            if x % 2 == 0:      # left encoders
                self.wc.d_left += ord(self.buffer[x])*LEFT_M_PER_TICK
            else:               # right encoders
                self.wc.d_right += ord(self.buffer[x])*RIGHT_M_PER_TICK
        return self.wc.d_left, self.wc.d_right

    def get_angle(self):
        """
        :return:
        """
        d_left, d_right = self.get_distance()
        return (d_left-d_right)/self.wc.L

    def get_d_delta(self):
        """
        :return:
        """
        d_left, d_right = self.get_distance()
        return (d_left + d_right)/2

    def get_velocity(self):
        # Get latest distance
        previous_d_left = self.wc.d_left
        previous_d_right = self.wc_d_right

        # Get updated distace
        d_left, d_right = self.get_distance()

        # Calc velocity
        vel_left = (d_left - previous_d_left)/self.wc.delta_t
        vel_right = (d_right - previous_d_right)/self.wc.delta_t

        return vel_left, vel_right



