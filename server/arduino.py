import serial
import glob

class ArduinoDisplay(object):
    def __init__(self):
        listing = glob.glob("/dev/tty.usb*")
        if not listing:
            raise Exception('No USB-Device found, aborting')
        while True:
            print 'Select USB-Device (Arduino)'
            print "\n".join(["%s. %s" % (i+1, v) for i, v in enumerate(listing)])
            choice = raw_input("> ")
            try:
                self.serial = serial.Serial(listing[int(choice)-1], 9600)
                break
            except:
                print 'Are you sure its that device?'
                pass

    def clear(self):
        self.serial.write(chr(0x18))

    def second_row(self):
        self.serial.write(chr(0x11))

    def first_row(self):
        self.serial.write(chr(0x12))

    def write(self, msg):
        map(self.serial.write,list(str(msg)))


