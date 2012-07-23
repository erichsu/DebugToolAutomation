'''
This is a subfunction of automation tool for adb command executing
'''

import subprocess

class AndroidSetting(object):
    '''
    classdocs
    '''

    def __init__(self, config=None):
        self.config = config
        self.options = ['battery', 'wifi', 'date', 'sms']
        
    def setup(self):
        #a None value indicates that the process hasn't terminated yet.
        status = None
        
        '''self._unlock_screen()'''
        
        for key in self.options:
            if key in self.config and self.config[key] != '':
                method = getattr(self, '_'+key)
                status = method(self.config[key])

        return status
    
    def _unlock_screen(self):
        #cmd = '%(adb)s shell input keyevent 82' % env
        #proc = subprocess.Popen(cmd.split())
        #return proc.wait()
        return 0
    
    def _date(self, datetime=''):
        print 'Setup date time'
        cmd = '%(adb)s wait-for-device shell date -s %(date)s' % self.config
        proc = subprocess.Popen(cmd.split())
        proc.wait()
    
    def _battery(self, volume='50'):
        print 'Setup battery'
        return 0
    
    def _sms(self, msg=''):
        print 'Setup sms'
        return 0
    
    def _wifi(self, on_off='off'):
        print 'Setup WIFI'
        return 0
        
if __name__ == "__main__":
    android_setting = AndroidSetting({'battery':'25', 'wifi':'off', 'date':'20101010', 'adb':'/Users/eric_hsu/Downloads/android-sdk-macosx/platform-tools/adb'})
    print 'result code: %s', android_setting.setup()
    
