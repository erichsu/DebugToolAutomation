"""
This is a Autmation script for Android App testing.
"""
import logging
import sys
import argparse
import os
import subprocess
import ConfigParser

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
        
        print 'Scanning TestCase in \n %s' % os.getcwd()
        test_list = self._get_test_list(os.getcwd())
        print 'There are %d Cases' % len(test_list)
        
        for test in test_list:
            name = os.path.basename(test)
            print '#### %s ####' % name
            tester = TestCaseHandler(TestCase(name))
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
        
        print '\n'
        
    def _setup_environment(self):
        """ TODO:
        1. launch the Emulator
        2. call the related tool to change the emulator env.
        """
        env = self.test_case.get_env()
        print env
        
    
    def _start_debug_mode(self):
        """ TODO: send intent message by adb shell command. """
        pass
    
    def _stop_debug_mode(self):
        """ TODO: send intent message by adb shell command. """
        pass
    
    def _trigger_test(self):
        cmd = self.test_case.get_test_script()
        proc = subprocess.Popen(cmd, cwd=self.test_case.path, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        print proc.stdout.read()
    
    def _collect_result(self):
        """ TODO: generate output folder """
        pass

class TestCase:
    def __init__(self, name):
        self.name = name
        self.path = os.path.join(os.getcwd(), name)
        self.config_path = os.path.join(self.path, 'config.ini')
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.config_path)
    
    def get_env(self):
        return self.config.items('environment')
    
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
    parser.add_argument('-c', '--config', action='store', dest='global_config', 
                        help='set the config file path')
    parser.add_argument('-p', '--prefix', action='store', dest='testcase_prefix', default='TestCase', 
                        help='set Test Case prefix, (default "TestCase")')
    parser.parse_args(namespace=automator)
    automator.run()
    

if __name__ == "__main__":
    #sys.argv += "-c C:\\testing\\path".split()
    main()
