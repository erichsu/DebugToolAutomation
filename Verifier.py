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
import re
import time,sqlite3
import ConfigParser
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import SubElement
import commands

class Verifier(object):
    def __init__(self, config_path=None, testcase=None):
        super(Verifier, self).__init__()
        self.config_path = config_path
        self.testcase = testcase
        
    def verify(self):
        report = []
        report += IniVerifier(self.config_path, self.testcase).verify()
        report += XmlVerifier(self.config_path, self.testcase).verify()
        report += DBVerifier(self.config_path, self.testcase).verify()
        report += LOGVerifier(self.config_path, self.testcase).verify()
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
            if not os.path.isfile(ini_path):
                result['file'] += ' - file not found'
                result['result'].append(('', '', 'File not found'))
                report.append(result)
                continue
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
            print report
        return report
    
    def _expected_data(self):
        parser = ConfigParser.ConfigParser()
        parser.read(self.config_path)
        return [ {'path':section, 'data':parser.items(section)} for section in parser.sections() if section.endswith('.ini') ]
    
#Only support Android Perference type.
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
            if not os.path.isfile(xml_path):
                result['file'] += ' - file not found'
                result['result'].append(('', '', 'File not found'))
                report.append(result)
                continue
            parser = ElementTree()
            tree = parser.parse(xml_path)
            itera =  tree.getiterator()
            for option in xml['data']:
                parser_name = option[0]
                parser_value = option[1]
                #print parser_name + ' | ' + parser_value
                for element in itera:
                    is_pass = False
                    has_option = False
                    #print 'value:', element.items()
                    if len(element.items())<0:
                        #is_pass = False
                        #result['result'].append((parser_name, parser_value, is_pass))
                        continue
                    elif len(element.items())<=1: #string
                        if str(element.get('name')).lower() in parser_name:
                            has_option = True
                            xml_parser_value = element.text
                            if self.isDecrypt(parser_name.upper()):
                                #print xml_parser_value
                                cmd = "java -jar DebugToolAES.jar " + xml_parser_value
                                xml_parser_value = commands.getoutput(cmd)
                                #print 'Decrypt content:' + str(xml_parser_value)
                            if parser_value in xml_parser_value:
                                is_pass = True
                                #print '**Find:', parser_name + ' ' + str(element.text)
                            #print "#string name:", element.get('name')
                            #print "#string value:", element.text
                            else:
                                is_pass = xml_parser_value
                        else:
                            is_pass = False
                    else: #int, boolean
                        if str(element.get('name')).lower() in parser_name:
                            has_option = True
                            if self.isDecrypt(parser_name.upper()):
                                cmd = "java -jar DebugToolAES.jar " + xml_parser_value
                                xml_parser_value = commands.getoutput(cmd)
                                #print 'Decrypt content:' + parser_value
                            if parser_value in element.get('value'):
                                is_pass = True
                                #print '**Find:', parser_name + ' ' + str(element.text)
                            #print "#value type:"
                            #print '#name:', element.get('name')
                            #print element.attrib
                            else:
                                is_pass = element.get('value')
                        else:
                            is_pass = False
                    if has_option:
                        result['result'].append((parser_name, parser_value, is_pass))
                        is_pass = False
                        has_option = False
        
            report.append(result)
        return report

    def isDecrypt(self, name):
        def_type = ['BIZ_TYPE', 'EOLKEY', 'EXPIREDATE', 'AUTORENEW', 'SUPERKEY', 'UID', 'LICENSE_STATUS', 'ENCRYPT_PASSWORD']
        try:
            result = def_type.index(name)
            #print 'isDecrypt:' + name
            return True
        except ValueError:
            return False
    
    def _expected_data(self):
        parser = ConfigParser.ConfigParser()
        parser.read(self.config_path)
        return [ {'path':section, 'data':parser.items(section)} for section in parser.sections() if section.endswith('.xml') ]

class DBVerifier:
    def __init__(self, config_path=None, testcase=None):
        self.config_path = config_path
        self.testcase = testcase
    
    def verify(self):
        report = []
        for db in self._expected_data():
            result = {}
            result['result'] = []
            result['file'] = os.path.basename(db['path'])
            result['type'] = 'db'
            print 'checking %s' % result['file']
            db_path = os.path.join(os.getcwd(), self.testcase, db['path'])
            if not os.path.isfile(db_path):
                result['file'] += ' - file not found'
                result['result'].append(('', '', 'File not found'))
                report.append(result)
                continue
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            db_table = ''
            for option in db['data']:
                if option[0] == 'table':
                    db_table = option[1]
                    result['file'] += '/' + db_table
                    continue    
                db_col = option[0]
                db_value = option[1]
                # print db_table + ' ' + db_col + ' ' + db_value
                db_str = 'select * FROM ' + db_table + ' WHERE ' + db_col + " LIKE '%" + db_value + "%'"
                #print db_str
                c.execute(db_str)
                data = c.fetchall()
                #print len(data)
            result['result'].append((db_col, db_value, len(data)))

            report.append(result)
        return report

    def _expected_data(self):
        parser = ConfigParser.ConfigParser()
        parser.read(self.config_path)
        return [ {'path':section, 'data':parser.items(section)} for section in parser.sections() if section.endswith('.db') ]

class LOGVerifier:
    def __init__(self, config_path=None, testcase=None):
        self.config_path = config_path
        self.testcase = testcase
    
    def verify(self):
        report = []
        for log in self._expected_data():
            result = {}
            result['result'] = []
            result['file'] = os.path.basename(log['path'])
            result['type'] = 'log'
            print 'checking %s' % result['file']
            
            parser_tag = ''
            parser_filter = ''
            log_path = os.path.join(os.getcwd(), self.testcase, log['path'])
            if not os.path.isfile(log_path):
                result['file'] += ' - file not found'
                result['result'].append(('', '', 'File not found'))
                report.append(result)
                continue
            parser_values = []
            parser_last_value = None
            for option in log['data']:
                if option[0] == 'tag':
                    parser_tag = option[1]
                elif option[0] == 'filter':
                    print 'filter:' + option[1]
                    parser_filter = option[1]
                    result['file'] += '[filter:' + option[1] +']'
                elif option[0] == 'value_last':
                    parser_last_value = option[1]
                elif 'value' in option[0]:
                    parser_values.insert(int(option[0][6:]), option[1])
            # print parser_values
            
            f = open(log_path)
            buf = f.readline()
            filter_contents = []
            find_count = 0
            while buf:
                m = re.search('(?P<time>\d*-\d* \d*:\d*:\d*.\d*) (?P<type>\w*)\/(?P<tag>\w\D*)(?P<pid>\d*)([)]?)(?P<content>.*)', buf)
                tag = m.group('tag')
                time = m.group('time')
                content = m.group('content').rstrip()
                find_tag = re.search(parser_tag, tag, re.IGNORECASE) 
                find_filter = re.search(parser_filter, content, re.IGNORECASE) 
                if find_tag and find_filter:
                    filter_contents.append((find_count, (content, time)))
                    find_count += 1
                buf = f.readline()
            f.close()
            for i, content in filter_contents:
                # print i
                if i < len(parser_values):
                    # print i, parser_values[i]
                    find_content = re.search(parser_values[i], content[0], re.IGNORECASE)
                    if find_content:
                        # print 'found'
                        result['result'].append(('value_' + str(i), parser_values[i], True))
                    else:
                        result['result'].append(('value_' + str(i), parser_values[i], content[1] + content[0]))
                elif i == len(filter_contents) - 1 and parser_last_value is not None:
                    find_content = re.search(parser_last_value, content[0], re.IGNORECASE)
                    if find_content:
                        # print 'found'
                        result['result'].append(('value_last', parser_last_value, True))
                    else:
                        result['result'].append(('value_last', parser_last_value, content[1] + content[0]))
            report.append(result)
        return report

    def _expected_data(self):
        parser = ConfigParser.ConfigParser()
        parser.read(self.config_path)
        return [ {'path':section, 'data':parser.items(section)} for section in parser.sections() if section.endswith('.log') ]

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
