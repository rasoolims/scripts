import re,os,sys,codecs
from urlparse import urlparse

rep = '' if len(sys.argv)<4 else sys.argv[3].strip()

writer = codecs.open(os.path.abspath(sys.argv[2]),'w')
c = 0
for line in codecs.open(os.path.abspath(sys.argv[1]),'r'):
	try:
		sen,label = line.strip().split('\t')
		out = ' '.join([e if not urlparse(e).scheme else rep for e in sen.split()])
		out = ' '.join([e  for e in out.split() if not e.startswith('@')])
		out = ' '.join([e  for e in out.split() if not e.startswith('@')])
		out = ' '.join([e  for e in out.split() if not e.startswith('#')])
		out = out.replace('&quot;','"').replace('&amp;','\'').replace('&lt;','<').replace('&gt;','>')
		writer.write(out+'\t'+label+'\n')
		c+=1
		if c%10000==0: sys.stdout.write(str(c)+'...')
	except:
		pass
		#print 'skipped',line

writer.close()
print 'done!'
