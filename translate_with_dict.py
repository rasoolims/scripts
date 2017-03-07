import os,sys,codecs,traceback
from urlparse import urlparse

trans = {line.strip().split()[0]:line.strip().split()[1] for line in codecs.open(os.path.abspath(sys.argv[1]),'r',encoding='utf-8')}
writer =codecs.open(os.path.abspath(sys.argv[3]),'w',encoding='utf-8')

for line in codecs.open(os.path.abspath(sys.argv[2]),'r',encoding='utf-8'):
	try:
		sen,label = line.strip().lower().split('\t')
		out = ' '.join([e if not urlparse(e).scheme else '' for e in sen.split()])
		out = ' '.join([e  for e in out.split() if not e.startswith('@')])
		out = ' '.join([e  for e in out.split() if not e.startswith('@')])
		out = ' '.join([e  for e in out.split() if not e.startswith('#')])
		sen = out.replace('&quot;','"').replace('&amp;','\'').replace('&lt;','<').replace('&gt;','>')
		output = []
		for word in sen.strip().split():
			if word in trans:
				output.append(word+'|||'+trans[word])
			else:
				output.append(word)
		writer.write(' '.join(output)+'\t'+label+'\n')
	except:
		print line
		traceback.print_exc()
		print line
		#sys.exit(1)
writer.close()