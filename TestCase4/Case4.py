#Case 4
#Drag down notification bar 

import time
import datetime
from time import gmtime, strftime

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()

#Launch TMMS console
settings_package = 'com.trendmicro.tmmssuite.consumer'
settings_activity = 'com.trendmicro.tmmssuite.consumer.login.ui.Login'
settings_runComponent = settings_package + '/' + settings_activity
device.startActivity(component=settings_runComponent)
# Press the Menu button
device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)
MonkeyRunner.sleep(2)
#Press About button
device.touch(400,660,"DOWN_AND_UP")
MonkeyRunner.sleep(2)
now=strftime("%Y-%m-%d-%H-%M-%S", gmtime())
# Takes a screenshot
result = device.takeSnapshot()
# Writes the screenshot to a file
result.writeToFile(r"shot-" + now +r".png",'png')

#Clean up UI
device.press('KEYCODE_HOME', MonkeyDevice.DOWN_AND_UP)

#Drag down notification bar
Start_point=(200,20)
End_point=(200,800)
device.drag(Start_point,End_point)
MonkeyRunner.sleep(2)
#Tap download link
device.touch(220,330,"DOWN_AND_UP")
MonkeyRunner.sleep(20)

device.drag(Start_point,End_point)
MonkeyRunner.sleep(2)
#Tap install link
device.touch(220,330,"DOWN_AND_UP")
MonkeyRunner.sleep(2)
#Click OK button
device.touch(130,570,"DOWN_AND_UP")
MonkeyRunner.sleep(3)
#Click Install button
device.touch(130,770,"DOWN_AND_UP")
MonkeyRunner.sleep(20)


#Launch TMMS console
settings_package = 'com.trendmicro.tmmssuite.consumer'
settings_activity = 'com.trendmicro.tmmssuite.consumer.login.ui.Login'
settings_runComponent = settings_package + '/' + settings_activity
device.startActivity(component=settings_runComponent)
# Press the Menu button
device.press('KEYCODE_MENU', MonkeyDevice.DOWN_AND_UP)
MonkeyRunner.sleep(2)
#Press About button
device.touch(400,660,"DOWN_AND_UP")
MonkeyRunner.sleep(3)
now=strftime("%Y-%m-%d-%H-%M-%S", gmtime())
# Takes a screenshot
result = device.takeSnapshot()
# Writes the screenshot to a file
result.writeToFile(r"shot-" + now +r".png",'png')


#Clean up UI
#device.press('KEYCODE_HOME', MonkeyDevice.DOWN_AND_UP)