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
        global T
        T = 1000
        self.autoWC = AutoWC()
        self.autoWC.wc.delta_t = T/1000

        interface = gtk.Builder()
        interface.add_from_file('AutoWC_GUI.glade')
        interface.connect_signals(self)

        self.Interface = interface.get_object('mainWindow')
        self.Interface.show()

        self.myPort = interface.get_object('entryPort')
        self.myStatus = interface.get_object('lbStatus')

        self.txtTicks = interface.get_object('textTicks')

        self.LRSignal = interface.get_object('adjustmentLR')
        self.FBSignal = interface.get_object('adjustmentFB')

        self.entryDistance = interface.get_object('entryDistance')
        self.entryAngle = interface.get_object('entryAngle')
        self.entryVelocity = interface.get_object('entryVelocity')

        self.cbtnStop = interface.get_object('cbtnStop')
        self.entryStop = interface.get_object('entryStop')


    def on_mainWindow_destroy(self,widget):
        try:
            self.autoWC.stop_wc()
            self.autoWC.serial.close_port()
        except AttributeError:
            pass
        gtk.mainquit()

    def on_btnRun_clicked(self, widget):
        self.autoWC.send_package('a', self.FBSignal.get_value())
        self.autoWC.send_package('b', self.LRSignal.get_value())

    def on_btnStop_clicked(self,widget):
        self.autoWC.stop_wc()
        self.FBSignal.set_value(2.5)
        self.LRSignal.set_value(2.5)

    def on_btnConnect_clicked(self,widget):
        try:
            self.autoWC.serial.open_port(self.myPort.get_text())
            self.myStatus.set_text("CONNECTED")
            self.timeout_handler_id = gtk.timeout_add(T, self.timer) #timeloop
        except:
            print "FAIL"

    def timer(self):
        self.txtTicks.set_text('')

        self.autoWC.update_buffer()
        self.autoWC.update_wc_info()

        for x in range (1,len(self.autoWC.buffer)):
            if x%2==0:
                self.txtTicks.insert_at_cursor(str(ord(self.autoWC.buffer[x]))+'\n')
            else:
                self.txtTicks.insert_at_cursor(str(ord(self.autoWC.buffer[x]))+'\t')

        self.d_left, self.d_right  = self.autoWC.get_distance()
        distance = 'd_left: %.2f\td_right: %.2f' % (self.d_left, self.d_right)
        self.entryDistance.set_text(distance)

        self.vel_left, self.vel_right = self.autoWC.get_velocity()
        velocity = 'v_left: %.2f\tv_right: %.2f' % (self.vel_left, self.vel_right)
        self.entryVelocity.set_text(velocity)

        self.entryAngle.set_text(str(self.autoWC.get_angle()))

        if self.cbtnStop.get_active() and self.entryStop.get_text() != '':
            self.stop_after(int(self.entryStop.get_text()))

        if self.vel_left == 0 and  self.vel_right == 0:
            self.autoWC.wipe_wc()

        return gtk.TRUE

    def on_btnFoward_clicked(self, widget):
        self.autoWC.send_package('a', 2)
        self.autoWC.send_package('b', 2.5)

        self.FBSignal.set_value(2)
        self.LRSignal.set_value(2.5)

    def on_btnBack_clicked(self, widget):
        self.autoWC.send_package('a', 3)
        self.autoWC.send_package('b', 2.5)

        self.FBSignal.set_value(3)
        self.LRSignal.set_value(2.5)

    def on_btnLeft_clicked(self, widget):
        self.autoWC.send_package('a', 2.5)
        self.autoWC.send_package('b', 3)

        self.FBSignal.set_value(2.5)
        self.LRSignal.set_value(3)


    def on_btnRight_clicked(self, widget):
        self.autoWC.send_package('a', 2.5)
        self.autoWC.send_package('b', 2)

        self.FBSignal.set_value(2.5)
        self.LRSignal.set_value(2)


    def stop_after(self, distance):
        if self.autoWC.wc.d_delta > distance:
            self.autoWC.stop_wc()


if __name__ == "__main__":
    mainProgram()
    gtk.main()