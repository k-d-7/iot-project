import time
from datetime import datetime
from mqtt import MQTTClient
import os
from dotenv import load_dotenv
from rs485 import *
import config
import json
import schedule
import scheduling
import fsm_irrigation

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

SCHEDULE_TAG = "schedulerRunning"



def processMQTT(data):
    data = json.loads(data)
    print(data)
    if data["action"] == "Create":
        print("Creating new scheduling ...")
        scheduleObject = scheduling.Scheduler(
            data["name"],
            data["area"],
            data["mixer1"],
            data["mixer2"],
            data["mixer3"],
            data["startTime"],
            data["endTime"],
            data["frequency"],
            data["date"],
            data["isActive"],
            data["cycle"]
        )
        config.schedulingList.append(scheduleObject)
        config.isRunningList.append(False)
        print("Create new scheduling name " + str(scheduleObject.name) + " successfully!")
    elif data["action"] == "Edit":
        print("Editing scheduling name " + str(data["name"]) + " ...")
        isEdited = False
        for i in config.schedulingList:
            if i.name == data["name"]:
                i.setScheduler(
                    data["name"],
                    data["area"],
                    data["mixer1"],
                    data["mixer2"],
                    data["mixer3"],
                    data["startTime"],
                    data["endTime"],
                    data["frequency"],
                    data["date"],
                    data["isActive"],
                    data["cycle"]
                )
                isEdited = True
        if isEdited == True:
            print("Edit scheduling name " + str(data["name"]) + " successfully!")
            config.mqttClient.publishMessage("kd77/feeds/notification", "Edit scheduling name " + str(data["name"]) + " successfully!")
        else:
            print("Edit scheduling name " + str(data["name"]) + " failed!")
            config.mqttClient.publishMessage("kd77/feeds/notification", "Edit scheduling name " + str(data["name"]) + " failed!")
    elif data["action"] == "Delete":
        print("Delete scheduling name " + str(data["name"]) + " ...")
        isDeleted = False
        for i in config.schedulingList:
            if i.name == data["name"]:
                config.schedulingList.remove(i)
                isDeleted = True
                config.isRunningList.remove(i)
        if isDeleted == True:
            print("Delete scheduling name " + str(data["name"]) + " successfully!")
            config.mqttClient.publishMessage("kd77/feeds/notification", "Delete scheduling name " + str(data["name"]) + " successfully!")
        else:
            print("Delete scheduler name " + str(data["name"]) + " failed!")
            config.mqttClient.publishMessage("kd77/feeds/notification", "Delete scheduling name " + str(data["name"]) + " failed!")

def endScheduling(index):
    schedule.clear(SCHEDULE_TAG)
    config.isRunningList = False
    config.mqttClient.publishMessage("kd77/feeds/notification", "Scheduling name " + config.schedulingList[index].name + " has been completed!")
    if config.schedulingList[index].frequency == "Once":
        print("Removing scheduling " + str(config.schedulingList[index].name) + " ..."  )
        config.schedulingList.remove(index)
        config.isRunningList.remove(index)
        
def runFSM(index):
    if fsm_irrigation.fsmIrrigation(index):
        print("End FSM by returning")
        # schedule.clear(SCHEDULE_TAG)
        # config.isRunningList = False
        # config.mqttClient.publish("kd77/feeds/notification", "Scheduling name " + config.schedulingList[index].name + " has been completed!")
        endScheduling(index)
        

def checkScheduling():
    currentTime = datetime.now()
    dayOfWeek = currentTime.strftime("%A")
    for i in range (len(config.schedulingList)):
        if dayOfWeek in config.schedulingList[i].date:
            currentHour = currentTime.hour
            currentMinute = currentTime.minute
            start_time = config.schedulingList[i].startTime.split(":")
            end_time = config.schedulingList[i].endTime.split(":")
            if currentHour == int(start_time[0]) and currentMinute == int(start_time[1]):
                if config.schedulingList[i].isActive == "1":
                    if config.isRunningList[i] == False :
                        print("Starting scheduling " + str(config.schedulingList[i].name) + " ...")
                        config.STATE = config.IDLE
                        config.cycle = config.schedulingList[i].cycle
                        schedule.every(1).seconds.do(runFSM, i).tag(SCHEDULE_TAG)
                        config.isRunningList[i] = True
                else:
                    continue
            elif currentHour == int(end_time[0]) and currentMinute == int(end_time[1]):
                if config.schedulingList[i].isActive == "1":
                    if config.isRunningList[i] == True:
                        print("Stopping scheduling " + str(config.schedulingList[i].name) + " ...")
                        # schedule.clear(SCHEDULE_TAG)
                        # config.isRunningList = False
                        endScheduling(i)
                else:
                    continue          
        else: 
            continue

temp = schedule.every(30).seconds.do(readTemperature)
humid = schedule.every(30).seconds.do(readMoisture)
schedule.every(10).seconds.do(checkScheduling)
        

def printschedulingList():
    print("Scheduler List:")
    for i in config.schedulingList:
        print("Name: " + i.name)
        print("Area: " + str(i.area))
        print("Mixer1: " + str(i.mixer1))
        print("Mixer2: " + str(i.mixer2))
        print("Mixer3: " + str(i.mixer3))
        print("Start Time: " + i.startTime)
        print("End Time: " + i.endTime)
        print("Active: " + i.frequency)
        print("Date: ")
        print(i.date)
        print("=====================================")
    print(".......................................")


config.mqttClient = MQTTClient(MQTT_SERVER, MQTT_PORT, TOPICS, MQTT_USERNAME, MQTT_PASSWORD)
config.mqttClient.setRecvCallBack(processMQTT)
config.mqttClient.connect()

count = 10

while True:
    # if count == 0:
    #     printschedulingList()
    #     count = 10
    #     # if temp.last_run_result:
    #     #     mqttClient.publishMessage("kd77/feeds/temperature", temp.last_run_result)
    #     # if humid.last_run_result:
    #     #     mqttClient.publishMessage("kd77/feeds/moisture", humid.last_run_result)
    # count -= 1
    schedule.run_pending()
    time.sleep(1)
    

        
