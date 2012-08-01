#Case 7
#Start Optimize button in Longevity main UI 

import time
import datetime
from time import gmtime, strftime

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()
#Open Longevity main UI
settings_package = 'com.trendmicro.mobileutilities.optimizer'
#settings_activity = 'com.trendmicro.mobileutilities.optimizer.ui.OptimizerMainEntry'
settings_activity = 'com.trendmicro.mobileutilities.optimizer.ui.WelcomePageActivity'
settings_runComponent = settings_package + '/' + settings_activity
device.startActivity(component=settings_runComponent)
MonkeyRunner.sleep(5)

#Press Optimize button
device.touch(200,700,"DOWN_AND_UP")
MonkeyRunner.sleep(5)
#Press Switch off Wi-Fi button
device.touch(50,390,"DOWN_AND_UP")
#Press Switch off Bluetooth button
device.touch(50,440,"DOWN_AND_UP")
#Press Reduce Darkness button
device.touch(50,480,"DOWN_AND_UP")
#Press Darken screen after 15 seconds button
device.touch(50,540,"DOWN_AND_UP")
MonkeyRunner.sleep(5)
#Press continue button
device.touch(240,750,"DOWN_AND_UP")
MonkeyRunner.sleep(15)

# now=strftime("%Y-%m-%d-%H-%M-%S", gmtime())


# Takes a screenshot
result = device.takeSnapshot()

# Writes the screenshot to a file
result.writeToFile(r"screenshot.png",'png')
