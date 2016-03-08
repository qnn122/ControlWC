from AutoWC import AutoWC
from WheelchairModel import WheelchairModel
from PID import PID
import pygtk
pygtk.require("2.0")
import gtk


class MainProgram:
    """This main class handles UI objects' behaviours
    """
    def __init__(self):
        # Time for timer
        global T
        T = 1000

        # For debugging
        global _debug
        _debug = False

        # For PID
        # TODO: Add GUI to tune K
        global Kp, Ki, Kd
        Kp = 3.0
        Ki = 0.4
        Kd = 1.2
        self.p = PID(3.0, 0.4, 1.2)
        self.p.setPoint(0)

        # Initialize AutoWC and WheelchairModel
        self.autoWC = AutoWC()
        self.wc = WheelchairModel()
        self.wc.delta_t = T / 1000.

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

        self.cbtnStop_distance = interface.get_object('cbtnStop_distance')
        self.cbtnStop_angle = interface.get_object('cbtnStop_angle')
        self.entryStop_distance = interface.get_object('entryStop_distance')
        self.entryStop_angle = interface.get_object('entryStop_angle')

    ##############################
    # Window
    ##############################
    def on_mainWindow_destroy(self, widget):
        try:
            self.autoWC.stop_wc()
            self.autoWC.serial.close_port()
        except AttributeError:
            pass
        gtk.mainquit()

    ##############################
    # Timer
    ##############################
    def timer(self):
        # Get data from serial port memory
        self.autoWC.update_buffer()

        # Update wheelchair info (from the buffer)
        self.wc.update_wc_info(self.autoWC.buffer)

        # Show numbers of ticks (for debugging)
        if _debug:
            self.txtTicks.set_text('')
            for x in range(1, len(self.autoWC.buffer)):
                if x % 2 == 0:
                    self.txtTicks.insert_at_cursor(str(ord(self.autoWC.buffer[x])) + '\n')
                else:
                    self.txtTicks.insert_at_cursor(str(ord(self.autoWC.buffer[x])) + '\t')

        # Display distance
        d_left, d_right = self.wc.get_distance()
        distance = 'Left: %.2f\tRight: %.2f' % (d_left, d_right)
        self.entryDistance.set_text(distance)

        # Display velocity
        vel_left, vel_right = self.wc.get_velocity()
        velocity = 'Left: %.2f\tRight: %.2f' % (vel_left, vel_right)
        self.entryVelocity.set_text(velocity)

        # Display angle
        self.entryAngle.set_text(str(self.wc.get_angle()))
        newTheta = self.p.update(self.wc.get_angle())
        # TODO: somehow adjust analog output using this newTheta

        # Stop if reaches given distance
        if self.cbtnStop_distance.get_active() and self.entryStop_distance.get_text() != '':
            self.stop_after_distance(int(self.entryStop_distance.get_text()))

        # Stop if reaches given angle
        if self.cbtnStop_angle.get_active() and self.entryStop_angle.get_text() != '':
            self.stop_after_angle(int(self.entryStop_angle.get_text()))

        return gtk.TRUE

    ##############################
    # Buttons
    ##############################
    def on_btnRun_clicked(self, widget):
        self.autoWC.send_package('a', self.FBSignal.get_value())
        self.autoWC.send_package('b', self.LRSignal.get_value())

    def on_btnStop_clicked(self,widget):
        self.autoWC.stop_wc()
        self.FBSignal.set_value(2.5)
        self.LRSignal.set_value(2.5)

    def on_btnReset_clicked(self,widget):
        self.wc.wipe_wc()

    def on_btnConnect_clicked(self,widget):
        """Connect to serial port, start Timer
        """
        try:
            self.autoWC.serial.open_port(self.myPort.get_text())
            self.myStatus.set_text("CONNECTED")
        except:
            print "FAIL to Connect to Serial Port."

        try:
            self.timeout_handler_id = gtk.timeout_add(T, self.timer)    # time loop
        except:
            print "Timer encounters problems."


    def on_btnFoward_clicked(self, widget):
        # Send commands to wc
        self.autoWC.send_package('a', 2)
        self.autoWC.send_package('b', 2.5)

        # Re-adjust GUI
        self.FBSignal.set_value(2)
        self.LRSignal.set_value(2.5)

    def on_btnBack_clicked(self, widget):
        # Send commands to wc
        self.autoWC.send_package('a', 3)
        self.autoWC.send_package('b', 2.5)

        # Re-adjust GUI
        self.FBSignal.set_value(3)
        self.LRSignal.set_value(2.5)

    def on_btnLeft_clicked(self, widget):
        # Send commands to wc
        self.autoWC.send_package('a', 2.5)
        self.autoWC.send_package('b', 3.2)

        # Re-adjust GUI
        self.FBSignal.set_value(2.5)
        self.LRSignal.set_value(3.2)


    def on_btnRight_clicked(self, widget):
        # Send commands to wc
        self.autoWC.send_package('a', 2.5)
        self.autoWC.send_package('b', 1.8)

        # Re-adjust GUI
        self.FBSignal.set_value(2.5)
        self.LRSignal.set_value(1.8)

    def stop_after_distance(self, distance):
        if self.wc.d_delta > distance:
            self.autoWC.stop_wc()

    def stop_after_angle(self, angle):
        if self.wc.theta_sum > angle:
            self.autoWC.stop_wc()

        # Reset angle
        self.wc.theta_sum = 0

    # TODO: Add PID to stabilize wheelchair movement. SetPoint: theta = 0


if __name__ == "__main__":
    MainProgram()
    gtk.main()