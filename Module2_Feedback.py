"""
In this module, a feedback monitor is added.
The feedback block will regularly (through a timer) read the number
of ticks of 2 wheels and display them on the GUI. The # of tick tells
us how fast the wheelchair truly is since the real velocity of the
wheelchair depends on many factors, e.g. weight of the user.

Control Wheelchair via serial port.
User input a pair of value which control 2 channels of the wheelchar.
Each value should fall in the range between 1(V) and 3.9(V).
The middle value, 2.5V, causes motor to stop.

Channel 1:
        Forward                   Backward
1V  --------------  2.5V  ----------------- 3.9 V

Channel 2:
        Right                   Left
1V  --------------  2.5V  ----------------- 3.9 V
"""
import pygtk
pygtk.require("2.0")
import gtk
import serial
import time
import gobject


class SendCommand:

    def __init__(self):
        interface = gtk.Builder()
        interface.add_from_file('Module2_FeedbackGUI.glade')
        interface.connect_signals(self)

        self.Interface = interface.get_object('mainWindow')
        self.Interface.show()

        self.myPort = interface.get_object('entryPort')
        self.myStatus = interface.get_object('lbStatus')

        self.LeftTick = interface.get_object('txtLeft')
        self.RightTick = interface.get_object('txtRight')

        self.leftBuffer = self.LeftTick.get_buffer()
        self.rightBuffer = self.RightTick.get_buffer()

        self.LRSignal = interface.get_object('scaleLR')
        self.FBSignal = interface.get_object('scaleFB')

    def on_mainWindow_destroy(self,widget):
        if hasattr(self, 'ser'):
            if self.ser.isOpen():
                self.ser.write(chr(120))    # Make sure the wc stops before closing the port
                self.ser.close()
        else:
            print "Serial port has never been created. Terminate the program."
        gtk.main_quit()

    def on_btnRun_click(self,widget):
        voltA = float(self.FBSignal.get_value_pos())
        voltB = float(self.LRSignal.get_value_pos())
        ao = int((voltA-1)*80 + 0.5)
        bo = int((voltB-1)*80 + 0.5)

        # Send data
        self.ser.write(chr(234))
        self.ser.write(chr(ao))
        self.ser.write(chr(bo))

        # Display what was sent
        print "VoltA = %.2f     VoltB = %.2f" % (voltA, voltB)
        print "ao = %d          bo = %d" % (ao, bo)

    def on_btnConnect_clicked(self,widget):

        self.Port = self.myPort.get_text()
        self.ser = serial.Serial(port="COM"+self.Port,
                                 baudrate=19200,
                                 bytesize=serial.EIGHTBITS,
                                 parity=serial.PARITY_NONE,
                                 stopbits=serial.STOPBITS_ONE,
                                 timeout=1)
        print(self.ser.name)
        time.sleep(2)                   # Give time for microcontroller to prepare
        self.ser.flush()                # flush all data from memory
        hello = self.ser.read(100)      # read all data from memory (if any)
        print hello
        self.myStatus.set_text("CONNECTED")

        feedback = gobject.timeout_add(1000, self.update_tick()) #timeloop

    def update_tick(self):
        #get tick value from encoder
        self.leftSignal = '1'
        self.rightSignal = '2'

        #update_onscreen
        self.leftBuffer.insert_at_cursor(self.leftSignal)
        self.rightBuffer.insert_at_cursor(self.rightSignal)



if __name__ == "__main__":
    SendCommand()
    gtk.main()