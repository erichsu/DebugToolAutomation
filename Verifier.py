#!/usr/bin/env python
# encoding: utf-8
"""
Verifier.py

Created by Eric Hsu (RD-TW) on 2012-07-11.
Copyright (c) 2012. All rights reserved.
"""

import sys
import argparse
import os

import ConfigParser
from xml.etree.ElementTree import ElementTree

class Verifier(object):
    """docstring for Verifier"""
    def __init__(self, config_path=None, testcase=None):
        super(Verifier, self).__init__()
        self.config_path = config_path
        self.testcase = testcase
        
    def verify(self):
        """docstring for verify"""
        report = []
        report += IniVerifier(self.config_path, self.testcase).verify()
        report += XmlVerifier(self.config_path, self.testcase).verify()
        return report

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
            result['type'] = 'ini'
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
            report.append(result)
        return report
    
    def _expected_data(self):
        parser = ConfigParser.ConfigParser()
        parser.read(self.config_path)
        return [ {'path':section, 'data':parser.items(section)} for section in parser.sections() if section.endswith('.ini') ]
    

class XmlVerifier:
    def __init__(self, config_path=None, testcase=None):
        self.config_path = config_path
        self.testcase = testcase
    
    def verify(self):
        report = []
        for xml in self._expected_data():
            result = {}
            result['result'] = []
            result['file'] = os.path.basename(xml['path'])
            result['type'] = 'xml'
            print 'checking %s' % result['file']
            xml_path = os.path.join(os.getcwd(), self.testcase, xml['path'])
            parser = ElementTree()
            parser.parse(xml_path)
            """TODO: Hello! Jarvis"""

        return report
    
    def _expected_data(self):
        parser = ConfigParser.ConfigParser()
        parser.read(self.config_path)
        return [ {'path':section, 'data':parser.items(section)} for section in parser.sections() if section.endswith('.xml') ]

def main():
    verifier = Verifier()
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
    print verifier.verify()
    return 0

if __name__ == "__main__":
    sys.argv += '-c TestCase0/config.ini -r TestCase0'.split()
    sys.exit(main())
