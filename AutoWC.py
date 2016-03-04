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

    def send_package(self, channel, volt):
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

    def stop_wc(self):
        """Stop the wheelchair
        """
        self.send_package('a', 2.5)
        self.send_package('b', 2.5)

    def update_buffer(self):
        """Update buffer
        """
        self.buffer = self.serial.read_port()  # numbers of ticks of 2 encoders

    def update_wc_info(self):
        """Get TOTAL distance travelled
        :return:
        """
        #store old distance
        self.wc.p_d_left = self.wc.d_left
        self.wc.p_d_right = self.wc.d_right

        #update distance
        for x in range(len(self.buffer)):
            if x % 2 == 0:      # left encoders
                self.wc.d_left += ord(self.buffer[x])*LEFT_M_PER_TICK
            else:               # right encoders
                self.wc.d_right += ord(self.buffer[x])*RIGHT_M_PER_TICK
        self.wc.d_delta = (self.wc.d_left + self.wc.d_right) / 2

        #update angle
        self.wc.theta = (self.wc.d_left - self.wc.d_right)/self.wc.L

        #update velocity
        self.wc.vel_left = (self.wc.d_left - self.wc.p_d_left) / self.wc.delta_t
        self.wc.vel_right = (self.wc.d_right - self.wc.p_d_right) / self.wc.delta_t

    def get_distance(self):
        return self.wc.d_left, self.wc.d_right

    def get_angle(self):
        return self.wc.theta

    def get_d_delta(self):
        return self.wc.d_delta

    def get_velocity(self):
        return self.wc.vel_left, self.wc.vel_right

    def wipe_wc(self):
        # wc position
        self.wc.x = 0
        self.wc.y = 0
        self.wc.theta = 0

        # wc travel distance
        self.wc.d_left = 0
        self.wc.d_right= 0
        self.wc.d_delta = 0

        #wc latest distance
        self.wc.p_d_left = 0
        self.wc.p_d_right = 0

        # wheel velocity
        self.wc.vel_left = 0
        self.wc.vel_right = 0
        self.wc.vel_dt = 0


