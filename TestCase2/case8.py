#Case 8
#Enable/Disable JAF function 
 
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
settings_activity = 'com.trendmicro.mobileutilities.optimizer.ui.entry.Entry'
settings_runComponent = settings_package + '/' + settings_activity

print "Start Activity"
print settings_runComponent
device.startActivity(component=settings_runComponent)
MonkeyRunner.sleep(5)

#Press Optimize button
device.touch(200,530,"DOWN_AND_UP")

for x in range(15):
    MonkeyRunner.sleep(1)
    print ".",
    
#Press continue button
device.touch(230,750,"DOWN_AND_UP")
MonkeyRunner.sleep(3)

# now=strftime("%Y-%m-%d-%H-%M-%S", gmtime())
#Takes a screenshot

result = device.takeSnapshot()
# Writes the screenshot to a file
result.writeToFile(r"screenshot.png",'png')
print "Sucess!"
