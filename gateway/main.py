import time
from mqtt import MQTTClient
import os
from dotenv import load_dotenv
from rs485 import *

load_dotenv()
MQTT_SERVER = os.getenv("MQTT_SERVER")
MQTT_PORT = os.getenv("MQTT_PORT")
print(MQTT_PORT)

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
TOPICS = [
    "kd77/feeds/scheduler",
    "kd77/feeds/notification"
]



# def test(payload):
#     print("test: " + payload)


mqttClient = MQTTClient(MQTT_SERVER, MQTT_PORT, TOPICS, MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.setRecvCallBack(writeSerial)
mqttClient.connect()

while True:
    
    time.sleep(1)
