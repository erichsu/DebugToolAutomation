'''
This is a subfunction of automation tool for adb command executing
'''

import subprocess

class AdbFun(object):
    '''
    classdocs
    '''

    def __init__(self, global_config=None):
        self.global_config = global_config
        self.support_adb = ['battery', 'wifi', 'osdatetime', 'sms']
        
    def _expectedSetting(self):
        print self.global_config
        
        #a None value indicates that the process hasn't terminated yet.
        status = None
        
        '''self._unlock_screen()'''
        
        for key in self.support_adb:
            if key in self.global_config and self.global_config[key] != '':
                method = getattr(self, '_'+key)
                status = method(self.global_config[key])

        return status
    
    def _unlock_screen(self):
        cmd = '%(adb)s shell input keyevent 82' % env
        proc = subprocess.Popen(cmd.split())
        return proc.wait()
    
    def _osdatetime(self, datetime=''):
        print '_osdatetime'
        return 0
    
    def _battery(self, volume='50'):
        print '_battery'
        return 0
    
    def _sms(self, msg=''):
        print '_sms'
        return 0
    
    def _wifi(self, on_off='off'):
        print '_wifi'
        return 0
        
if __name__ == "__main__":
    af = AdbFun({'battery':'25', 'wifi':'off', 'osdatetime':''})
    print 'result code: %s', af._expectedSetting()
    