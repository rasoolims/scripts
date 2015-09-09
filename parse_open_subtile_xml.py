from __future__ import unicode_literals
from xml.dom import minidom
import codecs,os,sys
from fnmatch import fnmatch
import re


writer=codecs.open(os.path.abspath(sys.argv[2]),'w',encoding='utf-8')
#writer=codecs.open('/tmp/file.txt','w',encoding='utf-8')


path = os.path.abspath(sys.argv[1])+'/'


has_eng_char=False
if sys.argv[3]=='true':
   has_eng_char=True

#path='/Users/msr/Downloads/OpenSubtitles/OpenSubtitles2012-1/ja/'

for r,d,f in os.walk(path):
   for file in f:
      if fnmatch(file, '*.xml'):
         full_path= os.path.join(r,file)
         print full_path
         try:
            xmldoc=minidom.parse(full_path)

            document_node= xmldoc.firstChild 

            s_nodes=xmldoc.getElementsByTagName("s")
            #print x
            #print document_node.childNodes
            for ch in s_nodes:
               w_nodes=ch.getElementsByTagName("w")

               sentence=''
               for w_n in w_nodes:
                  sentence+=w_n.firstChild.data
                  sentence+=u' '
               sentence=sentence.strip()
               
               if u'& nbsp ;' != sentence:
                  sentence+='\n'

                 
               if not sentence.strip():
                  sentence=ch.firstChild.data.strip()
                  sentence+='\n'
               

               if u'@' in sentence or u'***' in sentence or u'===' in sentence or u'www' in sentence:
                  continue

               if not has_eng_char and re.search('[a-zA-Z]', sentence):
                  continue

               if has_eng_char and not re.search('[a-zA-Z]', sentence):
                  continue

               if sentence.strip():
                  writer.write(sentence)

         except:
            print 'ERROR!'




#writer.write(xmldoc.toxml())


   #print w_nodes
   #print ch
   #writer.write(ch.toxml())
writer.close()