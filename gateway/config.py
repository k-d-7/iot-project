schedulingList = []
isRunningList = []

mqttClient = None

IDLE = 0
MIXER1 = 1
MIXER2 = 2
MIXER3 = 3
PUMP_IN = 4
PUMP_OUT = 5
SELECTOR = 6
NEXT_CYCLE = 7

STATE = -1

mixer1Volume = 0
mixer2Volume = 0
mixer3Volume = 0
pumpInVolume = 0
pumpOutVolume = 0

cycle = 0

timer1 = 0
