import os,sys,codecs

sens=codecs.open(os.path.abspath(sys.argv[1]),'r').read().split('\n')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')

for sen in sens:
	new_sen=list()
	for x in sen.strip().split(' '):
		x.strip()
		if x:
			new_sen.append(x[0:x.rfind('_')]+'/'+x[x.rfind('_')+1:])
	writer.write(' '.join(new_sen)+'\n')
writer.flush()
writer.close()