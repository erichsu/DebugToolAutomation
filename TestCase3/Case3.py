#Case 3
#Change date and verfiy program version 

import time
import datetime
from time import gmtime, strftime

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()

#device.installPackage(r"d:\tmms\scripts\TMMS_Cellcom.apk")

#Open Date/Time Settings 
settings_package = 'com.android.settings'
settings_activity = '.DateTimeSettings'
settings_runComponent = settings_package + '/' + settings_activity
device.startActivity(component=settings_runComponent)
MonkeyRunner.sleep(2)
#Disable Automatic Date/Time
device.touch(430,120,"DOWN_AND_UP")
MonkeyRunner.sleep(2)
#Click Set Date
device.touch(285,230,"DOWN_AND_UP")
MonkeyRunner.sleep(2)
#Set to next day
device.touch(230,360,"DOWN_AND_UP")
MonkeyRunner.sleep(2)
#Click Set button
device.touch(150,570,"DOWN_AND_UP")
MonkeyRunner.sleep(2)


now=strftime("%Y-%m-%d-%H-%M-%S", gmtime())


# Takes a screenshot
result = device.takeSnapshot()

# Writes the screenshot to a file
result.writeToFile(r"shot-" + now +r".png",'png')

#Clean up UI
device.press('KEYCODE_HOME', MonkeyDevice.DOWN_AND_UP)