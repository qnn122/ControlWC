#!/usr/bin/env python

"""
Main program
"""

from GetDataSerial import Serial

class AutoWC:

    def __init__(self):
        self.arrayLeftTicks = None
        self.sumLeftTicks = None
        self.arrayRightTicks = None
        self.sumRightTicks = None

        self.serial = Serial()
        self.port = self.serial.ser

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

    def updateTicks(self, buffer):
        """
        update  arrayTicks to print
                sumTicks to calculate distance
        :param buffer: buffer from serial port
        """
        for x in range (0, len(buffer)):
            if x % 2 == 0:
                self.arrayLeftTicks[x] = str(ord(buffer[x]))
                self.sumLeftTicks += ord(buffer[x])
            else:
                self.arrayRightTicks[x] = str(ord(buffer[x]))
                self.sumRightTicks += ord(buffer[x])
