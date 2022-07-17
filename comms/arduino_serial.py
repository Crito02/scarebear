from email import message
import serial
import time

# TODO: dependancy injection

class ArduinoComm():
    def __init__(self):
        self.arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1)

    def read(self):
        data = []
        data.append(self.arduino.readline())
        while True:
            newData = self.arduino.readline()
            if newData == b'':
                break
            else:
                data.append(newData)
        return data

    def write(self, dir, speed):
        # Format for arduino "<dir(rad),speed>"
        message = "<"+str(dir)+","+str(speed)+">"
        self.arduino.write(bytes(message, 'utf-8'))