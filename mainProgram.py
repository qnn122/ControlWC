#!/usr/bin/env python

"""
    This is main program
"""
import pygtk
pygtk.require("2.0")
import gtk
from AutoWC import AutoWC

class mainProgram:

    def __init__(self):

        self.autoWC = AutoWC()

        interface = gtk.Builder()
        interface.add_from_file('AutoWC_GUI.glade')
        interface.connect_signals(self)

        self.Interface = interface.get_object('mainWindow')
        self.Interface.show()

        self.myPort = interface.get_object('entryPort')
        self.myStatus = interface.get_object('lbStatus')

        self.txtLeftTick = interface.get_object('textbufferLeft')
        self.txtRightTick = interface.get_object('textbufferRight')

        self.LRSignal = interface.get_object('adjustmentLR')
        self.FBSignal = interface.get_object('adjustmentFB')

        self.btnRun = interface.get_object('btnRun')
        self.entryDistance = interface.get_object('entryDistance')

    def on_mainWindow_destroy(self,widget):
        self.autoWC.serial.closePort()
        gtk.mainquit()

    def on_btnRun_clicked(self, widget):
        self.autoWC.sendPackage('a', self.FBSignal.get_value())
        self.autoWC.sendPackage('b', self.LRSignal.get_value())

    def on_btnStop_clicked(self,widget):
        self.autoWC.stopWC()
        self.FBSignal.set_value(2.5)
        self.LRSignal.set_value(2.5)

    def on_btnConnect_clicked(self,widget):
        self.autoWC.serial.openPort(self.myPort.get_text())
        self.myStatus.set_text("CONNECTED")
        self.timeout_handler_id = gtk.timeout_add(200, self.timer) #timeloop

    def timer(self):
        self.txtLeftTick.set_text('')
        self.txtRightTick.set_text('')

        self.autoWC.updateTicks()

        #for x in range(0, (len(self.autoWC.buffer)) / 2):
            #self.txtLeftTick.insert_at_cursor(self.autoWC.arrayLeftTicks[x]+'\n')
            #self.txtRightTick.insert_at_cursor(self.autoWC.arrayRightTicks[x]+'\n')
        distance = 'd_left: %.2f\td_right: %.2f' % (self.autoWC.wc.d_left, self.autoWC.wc.d_right)
        self.entryDistance.set_text(distance)

        #self.stop_1m()

        return gtk.TRUE

    def on_btnFoward_clicked(self, widget):
        self.autoWC.goFoward()

    def on_btnBack_clicked(self, widget):
        self.autoWC.goBack()

    def stop_1m(self):
        d = ord(self.entryDistance.get_text())
        if d > 1:
            self.autoWC.stopWC()


if __name__ == "__main__":
    mainProgram()
    gtk.main()