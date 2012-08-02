#Case 5
#Launch debug tool
import time
import datetime
from time import gmtime, strftime

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()
#Start TMMS main UI

settings_package = 'com.trendmicro.tmmssuite.consumer'
settings_activity = 'com.trendmicro.supporttool.ui.ToolModeActivity'
settings_runComponent = settings_package + '/' + settings_activity
device.startActivity(component=settings_runComponent)
#Long tap on TrendMicro icon for entering debug mode
#Start_point=(200,750)
#device.drag(Start_point,Start_point,5,1)
MonkeyRunner.sleep(2)
#Click turn on debug log
device.touch(200,120,"DOWN_AND_UP")
MonkeyRunner.sleep(3)
now=strftime("%Y-%m-%d-%H-%M-%S", gmtime())


# Takes a screenshot
result = device.takeSnapshot()

# Writes the screenshot to a file
# result.writeToFile(r"shot-" + now +r".png",'png')
result.writeToFile(r"screenshot.png",'png')