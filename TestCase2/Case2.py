#Case 2
#Launch TMMS and verfiy pattern version 

import time
import datetime
from time import gmtime, strftime

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()

#device.installPackage(r"d:\tmms\scripts\TMMS_HTC.apk")

#Trigger TMMS update
#settings_package = 'com.trendmicro.tmmspersonal.HTC'
settings_package = 'com.trendmicro.tmmssuite.consumer'
settings_activity = 'com.trendmicro.tmmssuite.antimalware.ui.TmmsUpdateActivity'
settings_runComponent = settings_package + '/' + settings_activity
device.startActivity(component=settings_runComponent)
MonkeyRunner.sleep(8)

#Open TMMS UI of Antimalware
settings_activity = 'com.trendmicro.tmmssuite.antimalware.ui.AntimalwareTab'
settings_runComponent = settings_package + '/' + settings_activity
#device.startActivity(component='com.trendmicro.tmmspersonal.HTC/com.trendmicro.tmmssuite.consumer.login.ui.Login')
device.startActivity(component=settings_runComponent)
MonkeyRunner.sleep(2)

# Press the Menu button
#device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)

#Press the Update tab
MonkeyRunner.sleep(2)
device.touch(250,180,"DOWN_AND_UP") 
MonkeyRunner.sleep(2)


now=strftime("%Y-%m-%d-%H-%M-%S", gmtime())


# Takes a screenshot
result = device.takeSnapshot()

# Writes the screenshot to a file
result.writeToFile(r"shot-" + now +r".png",'png')

#Clean up UI
device.press('KEYCODE_HOME', MonkeyDevice.DOWN_AND_UP)