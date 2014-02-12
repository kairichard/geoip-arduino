import serial


class ArduinoDisplay(object):
    def __init__(self):
        self.serial = serial.Serial('/dev/tty.usbmodemfa131', 9600)

    def clear(self):
        self.serial.write(chr(0x18))

    def second_row(self):
        self.serial.write(chr(0x11))

    def first_row(self):
        self.serial.write(chr(0x12))

    def write(self, msg):
        map(self.serial.write,list(str(msg)))


