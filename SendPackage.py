#!/usr/bin/env python

import pygtk
pygtk.require("2.0")
import gtk
import serial
import time


class SendPackage:

    def __init__(self):
        interface = gtk.Builder()
        interface.add_from_file('SendPackageGUI.glade')
        interface.connect_signals(self)

        self.Interface = interface.get_object('mainWindow')
        self.Interface.show()

        self.mych1 = interface.get_object('entryChannel1')
        self.mych2 = interface.get_object('entryInput')
        self.myPort = interface.get_object('entryPort')
        self.myStatus = interface.get_object('lbStatus')

    def on_mainWindow_destroy(self,widget):
        if hasattr(self, 'ser'):
            if self.ser.isOpen():
                self.ser.write(chr(120)) #Make sure the wc stops before closing the port
                self.ser.close()
        else:
            print "Serial port has never been created. Terminate the program."
        gtk.main_quit()

    def on_btnSend_clicked(self,widget):
        voltA = float(self.mych1.get_text())
        voltB = float(self.mych2.get_text())
        ao = int((voltA-1)*80 + 0.5)
        bo = int((voltB-1)*80 + 0.5)
        # self.ser.write(chr(234))
        # self.ser.write(chr(ao))
        self.ser.write(chr(bo))
        # Another way
        # self.ser.write(234)
        # self.ser.write(ao)
        # self.ser.write(bo)
        print "VoltA = %.2f     VoltB = %.2f" %(voltA, voltB)
        print "ao = %d          bo = %d" %(ao, bo)

    def on_btnConnect_clicked(self,widget):
        self.Port = self.myPort.get_text()
        self.ser = serial.Serial(port="COM"+self.Port,
                    baudrate=9600,
                    bytesize=serial.EIGHTBITS,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_ONE,
                    timeout=1)
        print(self.ser.name)
        time.sleep(2)   # Give time for Arduino to prepare
        self.ser.flush()
        hello = self.ser.read(100)
        print hello
        self.myStatus.set_text("CONNECTED")

if __name__ == "__main__":
    SendPackage()
    gtk.main()



