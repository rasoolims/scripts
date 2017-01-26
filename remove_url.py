import re,os,sys,codecs
from urlparse import urlparse

rep = '' if len(sys.argv)<4 else sys.argv[3].strip()

writer = codecs.open(os.path.abspath(sys.argv[2]),'w')
c = 0
for line in codecs.open(os.path.abspath(sys.argv[1]),'r'):
	writer.write(' '.join([e if not urlparse(e).scheme else rep for e in line.split()])+'\n')
	c+=1
	if c%10000==0: sys.stdout.write(str(c)+'...')

writer.close()
print 'done!'
