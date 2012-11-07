#!/usr/bin/env python
# encoding: utf-8
"""
Automator.py
This is a Autmation script for Android App testing.

Created by Eric Hsu (RD-TW) on 2012-07-11.
Copyright (c) 2012. All rights reserved.
"""

import logging
import sys
import argparse
import os
import subprocess
import time
import ConfigParser
import re

from AndroidSetting import AndroidSetting
from Verifier import Verifier
from ReportMaker import ReportMaker

class Automator:
    """ Main class for automation. """
    """ TODO: add log """
    def run(self):
        """
        1. scan the test folders
        2. pass the folders one by one to the TestHandler
        """
        print 'Initilizing...'        
        print 'GLOBAL_CONFIG = %s' % self.global_config
        print 'TESTCASE_PREFIX = %s' % self.testcase_prefix
        print 'DEVICE = %s' % self.device if self.device is not None else 'No device selected, using Virtual Deivce by config'
        print '\n'
        
        config = ConfigParser.ConfigParser()
        config.read(os.path.join(os.getcwd(), self.global_config))
        global_config = dict(config.items('defaults'))
        
        # Check Android SDK
        if not os.path.exists(global_config['android_sdk']):
            print 'Android SDK not found'
            raise EnvironmentError
        
        report_maker = ReportMaker()
        if self.testcase:
            name = self.testcase
            print '### %s ###' % name
            tester = TestCaseHandler(TestCase(name, global_config), self.device, report_maker)
            tester.run()
            
        else:
            print 'Scanning TestCase in \n %s' % os.getcwd()
            test_list = self._test_list(os.getcwd())
            test_list.sort()
            print 'There are %d TestCases' % len(test_list)
            print '\n'
        
            for test in test_list:
                name = os.path.basename(test)
                print '#### %s ####' % name
                tester = TestCaseHandler(TestCase(name, global_config), self.device, report_maker)
                tester.run()
        report_maker.finish()

    def _test_list(self, path_root):
        """ list folders with the name heading of TESTCASE_PREFIX. """
        return [ os.path.join(path_root, dir)
                for dir in os.listdir(path_root)
                if os.path.isdir(dir) and dir.startswith(self.testcase_prefix) ]
        
class TestCaseHandler:
    def __init__(self, test_case, device, report_maker):
        if isinstance(test_case, TestCase):
            self.device = device
            self.test_case = test_case
            self.report_maker = report_maker
            self.env = self.test_case.get_env()
        else:
            raise TypeError
    
    def run(self):
        print self.test_case.description()
        
        print '@Setup the environment for testing.'
        self._setup_environment()
        
        print '@Start Debug Tool.'
        self._start_debug_mode()
        
        print '@Start test script.'
        self._trigger_test()
        
        print '@Stop Debug Tool'
        self._stop_debug_mode()
        
        print '@Collect Data'
        self._collect_result()
        
        print '@Verify Data'
        self._verify()
        
        print '@Generate Report'
        self._report()
        
        print '\n'
        
    def _setup_environment(self):
        if self.device is None:
            ## check existing emulator
            avd_list = [ re.search('Name: (?P<avd_name>.*)', buf).group('avd_name') 
                         for buf in subprocess.check_output(('%(android)s list avd' % self.env).split()).split('\n')
                         if re.search('Name: (?P<avd_name>.*)', buf) ]
            # print avd_list
            cmd = '%(adb)s devices' % self.env
            if 'emulator-%(avd_port)s' % self.env in subprocess.check_output(cmd.split()).split():
                print 'Fetal Error: there is already emulator-%(avd_port)s, please select another emulator port for Automator' % self.env
                print 'Maybe you could just select this emulator by "python Automator.py -s emulator-%(avd_port)s"' % self.env
                raise EnvironmentError
            elif not '%(avd)s' % self.env in avd_list:
                print 'Fetal Error: No AVD "%(avd)s" found' % self.env
                raise EnvironmentError
            ## launch emulator
            print 'Launch emulator'
            cmd = '%(emulator)s -avd %(avd)s -port %(avd_port)s' % self.env
            self.proc_emu = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            time.sleep(5)
        
            ## wait for emulator
            max_retry = 10
            timeout = 0
            while True:
                print 'Waiting for emulator...'
                cmd = '%(adb)s shell getprop init.svc.bootanim' % self.env
                proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                if 'stopped' in proc.stdout.read():
                    break
                if timeout > max_retry:
                    self.proc_emu.terminate()
                    print 'Relaunch emulator'
                    cmd = '%(emulator)s -avd %(avd)s -port %(avd_port)s' % self.env
                    self.proc_emu = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                    timeout = 0
                    max_retry += 1
                time.sleep(5)
                timeout += 1
        else:
            cmd = '%(adb)s devices' % self.env
            if not self.device in subprocess.check_output(cmd.split()).split():
                print 'Fetal Error: there is no %s, please select another emulator port for Automator' % self.device
                raise EnvironmentError
            # use selected device by serial number.
            self.env['adb'] += ' -s ' + self.device
            
        ## setup env by adb shell
        print 'Setup environment'
        AndroidSetting(self.env).setup()
        
        ## install test apk
        if self.env.has_key('apk'):
            print 'Install test apk'
            cmd = '%(adb)s wait-for-device install -r %(apk)s' % self.env
            proc = subprocess.Popen(cmd.split(), cwd=self.test_case.path)
            proc.wait()
    
    def _start_debug_mode(self):
        """ Send STARTPUP_TASK intent to the debug service. """
        cmd = '%(adb)s wait-for-device shell am startservice -n %(package)s/%(service)s -a %(intent_start)s' % self.env
        proc = subprocess.Popen(cmd.split())
        proc.wait()
    
    def _stop_debug_mode(self):
        """ Send STOP_TASK intent to the debug service. """
        cmd = '%(adb)s wait-for-device shell am startservice -n %(package)s/%(service)s -a %(intent_stop)s' % self.env
        proc = subprocess.Popen(cmd.split())
        proc.wait()
        
        max_retry_count = 10
        retry_count = 0
        while True:
            cmd = '%(adb)s shell dumpsys activity service com.trendmicro.tmmssuite.consumer' % self.env
            proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            prepro = proc.communicate();
            proc.wait()
            #print prepro[0]
            retry_count+=1
            if prepro[0].find('BackendService')>0:
                print 'Wait, since Support tool still alived'
            
            if retry_count >= max_retry_count:
                print 'Waiting timeout, keep going...'
                break
            time.sleep(5)
        
    
    def _trigger_test(self):
        err_count = 0
        while True:
            cmd = self.test_case.get_test_script()
            proc = subprocess.Popen(cmd.split(), cwd=self.test_case.path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            ret = proc.communicate()
            if len(ret[0]) is 0:
                break
            elif err_count > 3:
                print 'Error too many times...pass this test.'
                break
            err_count += 1
            print 'Monkey Runner unknown error, retrying...'
            # print len(ret[0])
    
    def _collect_result(self):
        cmd = '%(adb)s wait-for-device pull %(log_path)s output' % self.env
        proc = subprocess.Popen(cmd.split(), cwd=self.test_case.path)
        proc.wait()
        if self.device is None:
            self.proc_emu.terminate()
        
    def _verify(self):
        self.result = Verifier(self.test_case.config_path, self.test_case.name).verify()
        
    def _report(self):
        self.report_maker.export_result(self.test_case.name, self.result)

class TestCase:
    def __init__(self, name, global_config=None):
        self.name = name
        self.path = os.path.join(os.getcwd(), name)
        self.config_path = os.path.join(self.path, 'config.ini')
        self.config = ConfigParser.ConfigParser(global_config)
        self.config.read(self.config_path)
    
    def get_env(self):
        return dict(self.config.items('environment'))
    
    def get_test_script(self):
        return self.config.get('test script', 'command')
        
    def description(self):
        return self.config.get('test script', 'description')

def main():
    automator = Automator()
    parser = argparse.ArgumentParser(description='Autmation script for Android App testing.')
    parser.add_argument('-v', '--version', action='version', version='Automator 1.0',
                        help='show the version info')
    parser.add_argument('-s', action='store', dest='device', 
                        help='connect to device by serial number, please use "adb devices" to check the device')
    parser.add_argument('-r', '--run', action='store', dest='testcase', 
                        help='assign specific test case')
    parser.add_argument('-c', '--config', action='store', dest='global_config', default='config.ini', 
                        help='set the config file path')
    parser.add_argument('-p', '--prefix', action='store', dest='testcase_prefix', default='TestCase', 
                        help='set Test Case prefix, (default "TestCase")')
    parser.parse_args(namespace=automator)
    automator.run()
    return 0

if __name__ == "__main__":
    # sys.argv += '-s 0149905B1900F009 -r TestCase2'.split()
    sys.argv += '-s emulator-5554 -r TestCase2'.split()
    # sys.argv += '-r TestCase2'.split()
    sys.exit(main())
