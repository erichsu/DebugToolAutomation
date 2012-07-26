#Case 1
#Install TMMS and setup Trend account

import time
import datetime
from time import gmtime, strftime

# Imports the monkeyrunner modules used by this program
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# Connects to the current device, returning a MonkeyDevice object
device = MonkeyRunner.waitForConnection()

#Install TMMS package
# device.installPackage(r"SupportTool-TMMS.apk")
# MonkeyRunner.sleep(60)

#Start TMMS main UI
#settings_package = 'com.trendmicro.tmmspersonal.Cellcom'
settings_package = 'com.trendmicro.tmmssuite.consumer'
settings_activity = 'com.trendmicro.tmmssuite.consumer.login.ui.Login'
settings_runComponent = settings_package + '/' + settings_activity

device.startActivity(component=settings_runComponent)

#Press Accept button of License Agreement
MonkeyRunner.sleep(5)
device.touch(130,550,"DOWN_AND_UP") 

#Press the Register button
MonkeyRunner.sleep(2)
device.touch(242,750,"DOWN_AND_UP") 
MonkeyRunner.sleep(2)
#Press username input box 
device.touch(240,430,"DOWN_AND_UP")
MonkeyRunner.sleep(2)
#Input username
device.type(r"shujen_sun@trend.com.tw")
MonkeyRunner.sleep(2)
#Press Done key 
device.touch(420,750,"DOWN_AND_UP") 
MonkeyRunner.sleep(2)
#Press password input box 
device.touch(240,430,"DOWN_AND_UP")
MonkeyRunner.sleep(2)
#Input password
device.type(r"osce1234")
MonkeyRunner.sleep(2)
#Press Done key 
device.touch(420,750,"DOWN_AND_UP") 
MonkeyRunner.sleep(2)
#Press Accept button of License Agreement
device.touch(130,550,"DOWN_AND_UP") 
MonkeyRunner.sleep(25)
# #Press Accept button of Device Administrator
# device.touch(150,550,"DOWN_AND_UP")
# MonkeyRunner.sleep(10) 
# #Press Activate button of Device Administrator
# device.touch(150,770,"DOWN_AND_UP")
# MonkeyRunner.sleep(2)
now=strftime("%Y-%m-%d-%H-%M-%S", gmtime())


# Takes a screenshot
result = device.takeSnapshot()

# Writes the screenshot to a file
result.writeToFile(r"shot-" + now +r".png",'png')

#Remove TMMS package
# device.removePackage(settings_package)
#MonkeyRunner.sleep(60)

#Clean up UI
#device.press('KEYCODE_HOME', MonkeyDevice.DOWN_AND_UP)