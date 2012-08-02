#Case 1
#Install TMMS and launch

import time
import datetime
from time import gmtime, strftime

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()

#Start TMMS main UI
settings_package = 'com.trendmicro.tmmssuite.consumer'
settings_activity = 'com.trendmicro.tmmssuite.consumer.login.ui.Login'
settings_runComponent = settings_package + '/' + settings_activity

device.startActivity(component=settings_runComponent)

# Takes a screenshot
result = device.takeSnapshot()

# Writes the screenshot to a file
result.writeToFile(r"screenshot.png",'png')

#Clean up UI
#device.press('KEYCODE_HOME', MonkeyDevice.DOWN_AND_UP)