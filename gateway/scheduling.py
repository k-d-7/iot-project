class Scheduler:
    def __init__(self, name, area, mixer1, mixer2, mixer3, startTime, endTime, frequency, date, isActive, cycle):
        self.name = name
        self.area = area
        self.mixer1 = mixer1
        self.mixer2 = mixer2
        self.mixer3 = mixer3
        self.startTime = startTime
        self.endTime = endTime
        self.frequency = frequency
        self.date = date
        self.isActive = isActive
        self.cycle = cycle

    def setScheduler(self, name, area, mixer1, mixer2, mixer3, startTime, endTime, frequency, date, isActive, cycle):
        self.name = name
        self.area = area
        self.mixer1 = mixer1
        self.mixer2 = mixer2
        self.mixer3 = mixer3
        self.start_time = startTime
        self.end_time = endTime
        self.frequency = frequency
        self.date = date
        self.isActive = isActive
        self.cycle = cycle
        
    def printScheduler(self):
        print("Name: " + self.name)
        print("Area: " + self.area)
        print("Mixer1: " + self.mixer1)
        print("Mixer2: " + self.mixer2)
        print("Mixer3: " + self.mixer3)
        print("Start Time: " + self.startTime)
        print("End Time: " + self.endTime)
        print("Active: " + self.frequency)
        print("Date: ")
        print(self.date)
        print("Cycles: " + self.cycle)  
        