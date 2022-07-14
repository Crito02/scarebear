import serial
import time
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, timeout=.1)
def write_read(x):
    data = []
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)

    data.append(arduino.readline())
    while data != None:
        newData = arduino.readline()
        if newData == b'':
            break
        else:
            data.append(newData)
    return data
while True:
    num = input("Enter line: ")
    value = write_read(num)
    print(value)