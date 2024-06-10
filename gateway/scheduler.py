class Scheduler:
    def __init__(self, name, area, nitrogen, phosphorus, potassium, start_time, end_time, active, date):
        self.name = ""
        self.area = -1
        self.nitrogen = 0
        self.phosphorus = 0
        self.potassium = 0
        self.start_time = ""
        self.end_time = ""
        self.active = "Once"
        self.date = []

    def setScheduler(self, name, area, nitrogen, phosphorus, potassium, start_time, end_time, active, date):
        self.name = name
        self.area = area
        self.nitrogen = nitrogen
        self.phosphorus = phosphorus
        self.potassium = potassium
        self.start_time = start_time
        self.end_time = end_time
        self.active = active
        self.date = date
        
    def printScheduler():
        print("Name: " + self.name)
        print("Area: " + self.area)
        print("Nitrogen: " + self.nitrogen)
        print("Phosphorus: " + self.phosphorus)
        print("Potassium: " + self.potassium)
        print("Start Time: " + self.start_time)
        print("End Time: " + self.end_time)
        print("Active: " + self.active)
        print("Date: " + self.date)
        