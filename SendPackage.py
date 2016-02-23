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

        self.myInput = interface.get_object('entryInput')
        self.myPort = interface.get_object('entryPort')
        self.myStatus = interface.get_object('lbStatus')

    def on_mainWindow_destroy(self,widget):
        self.ser.close()
        gtk.main_quit()

    def on_btnSend_clicked(self,widget):
        self.s = self.myInput.get_text()
        if self.s == 'start':
            self.ser.write('A')
        elif self.s == 'stop':
            self.ser.write('B')
        elif self.s == 'reverse':
            self.ser.write('C')
        else:
            print 'Command invalid'

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



