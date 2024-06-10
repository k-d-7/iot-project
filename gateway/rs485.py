print("Sensors and Actuators")

import time
import serial.tools.list_ports

def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    return commPort
    # return "/dev/ttyUSB1"

portName = "/dev/ttyUSB1"
print(portName)



try:
    ser = serial.Serial(port=portName, baudrate=115200)
    print("Open successfully")
except:
    print("Can not open the port")
    
relay_data = [
    {'ON': [1, 6, 0, 0, 0, 255, 200, 91], 'OFF': [1, 6, 0, 0, 0, 0, 136, 27]},
    {'ON': [2, 6, 0, 0, 0, 255, 200, 91], 'OFF': [2, 6, 0, 0, 0, 0, 136, 27]},
    {'ON': [3, 6, 0, 0, 0, 255, 200, 91], 'OFF': [3, 6, 0, 0, 0, 0, 136, 27]},
    {'ON': [4, 6, 0, 0, 0, 255, 200, 91], 'OFF': [4, 6, 0, 0, 0, 0, 136, 27]},
    {'ON': [5, 6, 0, 0, 0, 255, 200, 91], 'OFF': [5, 6, 0, 0, 0, 0, 136, 27]},
    {'ON': [6, 6, 0, 0, 0, 255, 200, 91], 'OFF': [6, 6, 0, 0, 0, 0, 136, 27]},
    {'ON': [7, 6, 0, 0, 0, 255, 200, 91], 'OFF': [7, 6, 0, 0, 0, 0, 136, 27]},
    {'ON': [8, 6, 0, 0, 0, 255, 200, 91], 'OFF': [8, 6, 0, 0, 0, 0, 136, 27]}
]

# relay1_ON = [1, 6, 0, 0, 0, 255, 200, 91]
# relay1_OFF = [1, 6, 0, 0, 0, 0, 136, 27]

# relay2_ON = [2, 6, 0, 0, 0, 255, 200, 91]
# relay2_OFF = [2, 6, 0, 0, 0, 0, 136, 27]

# relay3_ON = [3, 6, 0, 0, 0, 255, 200, 91]
# relay3_OFF = [3, 6, 0, 0, 0, 0, 136, 27]

# relay4_ON = [4, 6, 0, 0, 0, 255, 200, 91]
# relay4_OFF = [4, 6, 0, 0, 0, 0, 136, 27]

# relay5_ON = [5, 6, 0, 0, 0, 255, 200, 91]
# relay5_OFF = [5, 6, 0, 0, 0, 0, 136, 27]

# relay6_ON = [6, 6, 0, 0, 0, 255, 200, 91]
# relay6_OFF = [6, 6, 0, 0, 0, 0, 136, 27]

# relay7_ON = [7, 6, 0, 0, 0, 255, 200, 91]
# relay7_OFF = [7, 6, 0, 0, 0, 0, 136, 27]

# relay8_ON = [8, 6, 0, 0, 0, 255, 200, 91]
# relay8_OFF = [8, 6, 0, 0, 0, 0, 136, 27]

def setDevice(state, device):
    if state == True:
        ser.write(relay_data[device - 1]['ON'])
    else:
        ser.write(relay_data[device - 1]['OFF'])
    time.sleep(1)
    print(serial_read_data(ser))

while True:
    setDevice1(True, 2)
    time.sleep(2)
    setDevice1(False, 2)
    time.sleep(2)


def serial_read_data(ser):
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        out = ser.read(bytesToRead)
        data_array = [b for b in out]
        print(data_array)
        if len(data_array) >= 7:
            array_size = len(data_array)
            value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
            return value
        else:
            return -1
    return 0

soil_temperature =[1, 3, 0, 6, 0, 1, 100, 11]
def readTemperature():
    serial_read_data(ser)
    ser.write(soil_temperature)
    time.sleep(1)
    return serial_read_data(ser)

soil_moisture = [1, 3, 0, 7, 0, 1, 53, 203]
def readMoisture():
    serial_read_data(ser)
    ser.write(soil_moisture)
    time.sleep(1)
    return serial_read_data(ser)

while True:
    print("TEST SENSOR")
    print(readMoisture())
    time.sleep(1)
    print(readTemperature())
    time.sleep(1)