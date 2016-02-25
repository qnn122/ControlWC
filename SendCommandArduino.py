"""
    Establish serial connection and send some bytes to arduino
    Send commands to control step motor
"""

import serial
import time
from time import  sleep


ser = serial.Serial(port='COM7',
                    baudrate=9600,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1)
print(ser.name) # Confirm current serial port
#ser.open()      # Open port

# Input something to arduino
time.sleep(2)   # Give time for Arduino to prepare
ser.flush()
hello = ser.read(100)
print hello


def sendCommand(s):
    global ser
    if s == 'start':
        ser.write('A')
    elif s == 'stop':
        ser.write('B')
    elif s == 'reverse':
        ser.write('C')
    else:
        print 'Command invalid'
        return

while 1:
    s = raw_input("Enter something (press q to quit): ")
    if s == 'q':
        break
    else:
        sendCommand(s)
        print '*** Send: "%s"' % s

ser.close()


