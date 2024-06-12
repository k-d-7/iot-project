from datetime import datetime

currentTime = datetime.now()
dayOfWeek = currentTime.strftime("%A")
currentHour = currentTime.hour
currentMinute = currentTime.minute

print("Current time: %s" % currentTime)
print("Day of week: %s" % dayOfWeek)
print("Current hour: %s" % currentHour)
print("Current minute: %s" % currentMinute)
