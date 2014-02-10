import serial


class ArduinoDisplay(object):
    def __init__(self):
        self.serial = serial.Serial('/dev/tty.usbmodemfa131', 9600)

    def clear(self):
        self.serial.write(chr(0x18))

    def newline(self):
        self.serial.write(chr(0xA))

    def write(self, msg):
        map(self.serial.write,list(str(msg)))


