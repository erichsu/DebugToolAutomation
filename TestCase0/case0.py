#Case 0
#Start Longevity main UI 

import time
import datetime
from time import gmtime, strftime

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()
#Open Longevity main UI
settings_package = 'com.trendmicro.mobileutilities.optimizer'
settings_activity = 'com.trendmicro.mobileutilities.optimizer.ui.OptimizerMainEntry'
settings_runComponent = settings_package + '/' + settings_activity
device.startActivity(component=settings_runComponent)

# Takes a screenshot
result = device.takeSnapshot()

# Writes the screenshot to a file
result.writeToFile(r"screenshot.png",'png')