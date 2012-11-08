#Case 2
#Launch TMMS 3.0 and verfiy pattern version 

import time
import datetime
from time import gmtime, strftime

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()


#Open TMMS UI of Antimalware
settings_package = 'com.trendmicro.tmmssuite.consumer'
settings_activity = 'com.trendmicro.tmmssuite.consumer.scanner.threat.ThreatScannerMain'
settings_runComponent = settings_package + '/' + settings_activity
device.startActivity(component=settings_runComponent)
MonkeyRunner.sleep(5)

#Press the Update tab
device.touch(250,410,"DOWN_AND_UP") 
MonkeyRunner.sleep(5)

#Trigger TMMS update by click icon
device.touch(430,510,"DOWN_AND_UP") 
MonkeyRunner.sleep(20)
device.press('KEYCODE_BACK', MonkeyDevice.DOWN_AND_UP)

now=strftime("%Y-%m-%d-%H-%M-%S", gmtime())


# Takes a screenshot
result = device.takeSnapshot()

# Writes the screenshot to a file
result.writeToFile(r"shot-" + now +r".png",'png')

#Clean up UI
#device.press('KEYCODE_HOME', MonkeyDevice.DOWN_AND_UP)