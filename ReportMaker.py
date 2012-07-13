'''
Created on Jul 12, 2012

@author: weikun
'''

from xml.dom.minidom import Document
import subprocess

class ReportMaker():
    
    ispass = 'fail'
    
    def finish(self):
        pass
    
    def export_result(self, testcase, results=[]):
        global ispass
        ispass = 'pass'
        
        doc = Document()
        #root = self._add_tag(doc, doc, 'testcase')
        root = doc.createElement('testcase')
        doc.appendChild(root)
        
        self._set_tag_text(doc, root, "id", testcase)
        tagini = self._add_tag(doc, root, 'inis')
        tagdb = self._add_tag(doc, root, 'dbs')
        tagxml = self._add_tag(doc, root, 'xmls')
        
        for result in results:
            filename = result['file']
            filetype = result['type']
            conditionlist = result['result'] #tuple list
            
            print filetype
            seltag = None
            if filetype == 'ini':
                seltag = tagini
            elif filetype == 'db':
                seltag = tagdb
            elif filetype == 'xml':
                seltag = tagxml
            
            self._create_xml_by_result(doc, seltag, filename, filetype, conditionlist)
        
        print 'ready output'
        
        f = open('report/tmp/'+testcase+'_'+ispass+'.xml', 'w+')
        #f.write(doc.toprettyxml(indent = '  ', newl='\r\n', encoding='utf8'))
        f.write(doc.toxml(encoding='utf8'))
        f.close()
        
        cmd = './xslt.jar ./report/tmp'
        proc = subprocess.Popen(cmd.split())
        proc.wait()
        
    def _create_xml_by_result(self, root, doc, filename, filetype, conditionlist=()):
        
        tagfiletype = self._add_tag(root, doc, filetype)
        
        self._set_tag_text(root, tagfiletype, 'filename', filename)
        
        tagconds = self._add_tag(root, tagfiletype, 'conds')
        
        for cond in conditionlist:
            #[0]:key, [1]:value, [2]:status

            tagcond = self._add_tag(root, tagconds, 'cond')

            self._set_tag_text(root, tagcond, 'key', cond[0])
            self._set_tag_text(root, tagcond, 'value', cond[1])
            self._set_tag_text(root, tagcond, 'status', str(cond[2]))
            
            global ispass
            if str(cond[2]) != 'True':
                ispass = 'fail'
        
    def _set_tag_text(self, root, doc, key, value=''):
        newtag = root.createElement(key)
        newtag.appendChild(root.createTextNode(value))
        doc.appendChild(newtag)

    def _add_tag(self, root, doc, tagname):
        newtag = root.createElement(tagname)
        doc.appendChild(newtag)
        return newtag 

if __name__ == '__main__':
    reportmarker = ReportMaker()
    reportmarker.export_result('testcase1',
                                [{'file':'xxxx.ini',
                                  'type':'ini',
                                  'result':(
                                            ['ini.status','updated',True],
                                            ['ini.updatetime','20120713.123456','20120712.123456'])},
                                 {'file':'oooo.ini',
                                  'type':'ini',
                                  'result':(
                                            ['ini.status2','updated',True],
                                            ['ini.updatetime2','20120713.123456','20120712.123456'])},
                                 {'file':'xxxx.db',
                                  'type':'db',
                                  'result':(
                                            ['db.status','updated',True],
                                            ['db.updatetime','20120713.123456','20120712.123456'])}])

    