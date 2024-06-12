import config
import rs485

def fsmIrrigation(index):
    match config.STATE:
        case config.IDLE:
            print("In IDLE state")
            print("Change to Mixer 1 in " + str(config.timer1) + " !")
            if config.timer1 <= 0:
                config.STATE = config.MIXER1
                config.timer1 = 10
                config.mixer1Volume = config.schedulingList[index].mixer1
                config.mixer2Volume = config.schedulingList[index].mixer2
                config.mixer3Volume = config.schedulingList[index].mixer3
                config.pumpInVolume = config.mixer1Volume + config.mixer2Volume + config.mixer3Volume
                config.pumpOutVolume = config.mixer1Volume + config.mixer2Volume + config.mixer3Volume
                rs485.setDevice(True, 1)
            else:
                config.timer1 -= 1           
        case config.MIXER1:
            print("Pumping Mixer 1 ...")
            print("Remaining Volume is " + str(config.mixer1Volume) + ".")
            if config.timer1 <= 0  or config.mixer1Volume <=0:
                config.STATE = config.MIXER2
                config.timer1 = 10
                rs485.setDevice(False, 1)
                rs485.setDevice(True, 2)
            else:
                config.mixer1Volume -= 5
                config.timer1 -= 1           
        case config.MIXER2:
            print("Pumping Mixer 2 ...")
            print("Remaining Volume is " + str(config.mixer2Volume) + ".")
            if config.timer1 <= 0 or config.mixer2Volume <=0:
                config.STATE = config.MIXER3
                config.timer1 = 10
                rs485.setDevice(False, 2)
                rs485.setDevice(True, 3)
            else:
                config.mixer2Volume -= 5
                config.timer1 -= 1     
        case config.MIXER3:
            print("Pumping Mixer 3 ...")
            print("Remaining Volume is " + str(config.mixer3Volume) + ".")
            if config.timer1 <= 0 or config.mixer3Volume <=0:
                config.STATE = config.PUMP_IN
                config.timer1 = 20
                rs485.setDevice(False, 3)
                rs485.setDevice(True, 7)
            else:
                config.mixer3Volume -= 5
                config.timer1 -= 1            
        case config.PUMP_IN:
            print("Pumping In ...")
            print("Remaining Volume is " + str(config.pumpInVolume) + ".")
            if config.timer1 <= 0 or config.pumpInVolume <=0:
                config.STATE = config.SELECTOR
                config.timer1 = 2
                rs485.setDevice(False, 7)
            else:
                config.pumpInVolume -= 5
                config.timer1 -= 1            
        case config.PUMP_OUT:
            print("Pumping Out ...")
            print("Remaining Volume is " + str(config.pumpOutVolume) + ".")
            if config.timer1 <= 0 or config.pumpOutVolume <=0:
                config.STATE = config.NEXT_CYCLE
                config.timer1 = 3
                rs485.setDevice(False, 8)
                print("Current state after stop pumping out ---> " + str(config.STATE))
            else:
                config.pumpOutVolume -= 5
                config.timer1 -= 1            
        case config.SELECTOR:
            print("Selecting Area ...")
            if config.timer1 <= 0:
                print("Area " + str(config.schedulingList[index].area) + " is selected")
                config.STATE = config.PUMP_OUT
                config.timer1 = 20
                rs485.setDevice(True, config.schedulingList[index].area)
                rs485.setDevice(True, 8)
            else:
                config.timer1 -= 1           
        case config.NEXT_CYCLE:
            if config.timer1 <= 0:
                print("Finished One Cycle")
                config.cycle -= 1
                if config.cycle <= 0:
                    config.STATE = config.IDLE
                    config.timer1 = 5
                    print("Finished Irrigation")
                    return True
                else:
                    print("Change to Next cycle, " + str(config.cycle))
                    config.STATE = config.MIXER1
                    config.timer1 = 10
                    config.mixer1Volume = config.schedulingList[index].mixer1
                    config.mixer2Volume = config.schedulingList[index].mixer2
                    config.mixer3Volume = config.schedulingList[index].mixer3
                    config.pumpInVolume = config.mixer1Volume + config.mixer2Volume + config.mixer3Volume
                    config.pumpOutVolume = config.mixer1Volume + config.mixer2Volume + config.mixer3Volume
                    rs485.setDevice(False, config.schedulingList[index].area)
            else:
                config.timer1 -= 1