#!/usr/bin/env python
# encoding: utf-8
"""
Verifier.py

Created by Eric Hsu (RD-TW) on 2012-07-11.
Copyright (c) 2012. All rights reserved.
"""

import sys
import ConfigParser
import argparse
import os

class IniVerifier:
    def __init__(self, config_path=None, testcase=None):
        self.config_path = config_path
        self.testcase = testcase
    
    def verify(self):
        report = []
        for ini in self._expected_data():
            result = {}
            result['result'] = []
            result['file'] = os.path.basename(ini['path'])
            print 'checking %s' % result['file']
            ini_path = os.path.join(os.getcwd(), self.testcase, ini['path'])
            parser = ConfigParser.ConfigParser()
            parser.read(ini_path)
            for option in ini['data']:
                # print option
                has_option = False
                is_pass = False
                for section in parser.sections():
                    if parser.has_option(section, option[0]):
                        # print 'find option %s' % option[0]
                        has_option = True
                        if parser.get(section, option[0]) == option[1]:
                            # print 'pass'
                            is_pass = True
                        else:
                            # print 'fail:', parser.get(section, option[0])
                            is_pass = parser.get(section, option[0])
                if not has_option:
                    # print 'error, attribute %s not found' % option[0]
                    is_pass = 'n/a'
                    
                result['result'].append((option[0], option[1], is_pass))
        return report.append(result)
        
    def _expected_data(self):
        parser = ConfigParser.ConfigParser()
        parser.read(self.config_path)
        return [ {'path':section, 'data':parser.items(section)} for section in parser.sections() if section.endswith('.ini') ]

def main():
    verifier = IniVerifier()
    parser = argparse.ArgumentParser(description='Autmation script for Android App testing.')
    parser.add_argument('-v', '--version', action='version', version='Verifier 1.0',
                        help='show the version info')
    parser.add_argument('-r', '--run', action='store', dest='testcase', 
                        help='assign specific test case')
    parser.add_argument('-c', '--config', action='store', dest='config_path', default='config.ini', 
                        help='set the config file path')
    parser.add_argument('-p', '--prefix', action='store', dest='testcase_prefix', default='TestCase', 
                        help='set Test Case prefix, (default "TestCase")')
    parser.parse_args(namespace=verifier)
    verifier.verify()
    return 0

if __name__ == "__main__":
    sys.argv += '-c TestCase0/config.ini -r TestCase0'.split()
    sys.exit(main())
