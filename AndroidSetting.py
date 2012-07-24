#!/usr/bin/env python
# encoding: utf-8
"""
AndroidSetting.py

Created by Eric Hsu (RD-TW) on 2012-07-11.
Copyright (c) 2012. All rights reserved.
"""

import subprocess

class AndroidSetting(object):
    def __init__(self, config=None):
        self.config = config
        self.options = ['battery', 'wifi', 'date', 'sms']
        
    def setup(self):
        for option in self.options:
            if option in self.config and self.config[option] != '':
                method = getattr(self, '_' + option)
                status = method(self.config[option])
    
    def _unlock_screen(self):
        cmd = '%(adb)s shell input keyevent 82' % self.config
        proc = subprocess.Popen(cmd.split())
        return proc.wait()
    
    def _date(self, datetime=''):
        print 'Setup date time'
        cmd = '%(adb)s wait-for-device shell date -s %(date)s' % self.config
        # proc = subprocess.Popen(cmd.split())
        # proc.wait()
        print cmd
    
    def _battery(self, volume='50'):
        print 'Setup battery'
        cmd = '%(adb)s wait-for-device emu power ac on' % self.config
        # proc = subprocess.Popen(cmd.split())
        # proc.wait()
        print cmd
        
        cmd = '%(adb)s wait-for-device emu power status discharging' % self.config
        # proc = subprocess.Popen(cmd.split())
        # proc.wait()
        print cmd
        
        cmd = '%(adb)s wait-for-device emu power %s' % self.config
        # proc = subprocess.Popen(cmd.split())
        # proc.wait()
        print cmd
    
    def _sms(self, msg=''):
        print 'Setup sms'
        # ./adb emu sms send 886911123456 <text message>
    
    def _wifi(self, on_off='off'):
        print 'Setup WIFI'
        # ./adb emu gsm data <on|off>
        
if __name__ == "__main__":
    android_setting = AndroidSetting({'battery':'25', 'wifi':'off', 'date':'20101010', 'adb':'/Users/eric_hsu/Downloads/android-sdk-macosx/platform-tools/adb'})
    android_setting.setup()
    