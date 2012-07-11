"""
This is a Autmation script for Android App testing.
"""
import logging
import sys
import argparse
import os
import subprocess
import time
import ConfigParser

from AndroidSetting import AndroidSetting

class Automator():
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
        print '\n'
        
        config = ConfigParser.ConfigParser()
        config.read(os.path.join(os.getcwd(), self.global_config))
        global_config = dict(config.items('defaults'))
        
        if self.testcase:
            name = self.testcase
            print '### %s ###' % name
            tester = TestCaseHandler(TestCase(name, global_config))
            tester.run()
            
        else:
            print 'Scanning TestCase in \n %s' % os.getcwd()
            test_list = self._get_test_list(os.getcwd())
            print 'There are %d TestCases' % len(test_list)
            print '\n'
        
            for test in test_list:
                name = os.path.basename(test)
                print '#### %s ####' % name
                tester = TestCaseHandler(TestCase(name, global_config))
                tester.run()

    def _get_test_list(self, path_root):
        """ list folders with the name heading of TESTCASE_PREFIX. """
        return [ os.path.join(path_root, dir)
                for dir in os.listdir(path_root)
                if os.path.isdir(dir) and dir.startswith(self.testcase_prefix) ]
        
class TestCaseHandler:
    def __init__(self, test_case):
        if isinstance(test_case, TestCase):
            self.test_case = test_case
        else:
            raise TypeError
    
    def run(self):
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
        """ TODO: call the related tool to change the emulator env. """
        env = self.test_case.get_env()
        
        ## launch emulator
        print 'Launch emulator'
        cmd = '%(emulator)s -avd %(os)s' % env
        self.proc_emu = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        time.sleep(1)
        
        ## wait for emulator
        print 'Waiting for emulator...'
        while True:
            cmd = '%(adb)s wait-for-device shell getprop init.svc.bootanim' % env
            proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if 'stopped' in proc.stdout.read():
                break
            time.sleep(3)
                
        ## setup env by adb shell
        print 'Setup environment'
        AndroidSetting(env).setup()
        
        ## install test apk
        print 'Install test apk'
        cmd = '%(adb)s wait-for-device install -r %(apk)s' % env
        proc = subprocess.Popen(cmd.split(None, 4), cwd=self.test_case.path)
        proc.wait()
    
    def _start_debug_mode(self):
        """ Send STARTPUP_TASK intent to the debug service. """
        cmd = '%(adb)s wait-for-device shell am startservice -n %(package)s/%(service)s -a com.trendmicro.mobile.tool.STARTUP_TASK' % self.test_case.get_env()
        proc = subprocess.Popen(cmd.split())
        proc.wait()
    
    def _stop_debug_mode(self):
        """ Send STOP_TASK intent to the debug service. """
        cmd = '%(adb)s wait-for-device shell am startservice -n %(package)s/%(service)s -a com.trendmicro.mobile.tool.STOP_TASK' % self.test_case.get_env()
        proc = subprocess.Popen(cmd.split())
        proc.wait()
        
        """ TODO: make sure service is stopped fully, here use dumpsys command to check infinitely. """
        max_retry_count = 10
        retry_count = 0
        while True:
            cmd = '%(adb)s shell dumpsys activity service com.trendmicro.tmmssuite.consumer' % self.test_case.get_env()
            proc = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            prepro = proc.communicate();
            proc.wait()
            #print prepro[0]
            retry_count+=1
            if prepro[0].find('BackendService')>0:
                print 'continue, since backend still alived'
            
            if retry_count >= max_retry_count:
                print 'it is time to go'
                break
            time.sleep(1)
        print 'end...'
        
    
    def _trigger_test(self):
        cmd = self.test_case.get_test_script()
        proc = subprocess.Popen(cmd.split(), cwd=self.test_case.path)
        proc.wait()
    
    def _collect_result(self):
        """ TODO: use adb shell to get result in SD card folder """
        # cmd = '%(adb)s wait-for-device shell am startservice -n %(service)s -a com.trendmicro.mobile.tool.STOP_TASK' % self.test_case.get_env()
        # proc = subprocess.Popen(cmd.split())
        # proc.wait()
        self.proc_emu.terminate()
        
    def _verify(self):
        pass
        
    def _report(self):
        pass

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
        
    def get_expected_result(self):
        return self.config.items('expected result')
    
    def run(self):
        pass

def main():
    automator = Automator()
    parser = argparse.ArgumentParser(description='Autmation script for Android App testing.')
    parser.add_argument('-v', '--version', action='version', version='Automator 1.0',
                        help='show the version info')
    parser.add_argument('-r', '--run', action='store', dest='testcase', 
                        help='assign specific test case')
    parser.add_argument('-c', '--config', action='store', dest='global_config', default='config.ini', 
                        help='set the config file path')
    parser.add_argument('-p', '--prefix', action='store', dest='testcase_prefix', default='TestCase', 
                        help='set Test Case prefix, (default "TestCase")')
    parser.parse_args(namespace=automator)
    automator.run()
    

if __name__ == "__main__":
    sys.argv += "-r TestCase0".split()
    main()
