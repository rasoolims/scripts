import os,sys,codecs

sens=codecs.open(os.path.abspath(sys.argv[1]),'r').read().split('\n\n')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')

for sen in sens:
	lines=sen.strip().split('\n')
	words=list()
	for l in lines:
		if l.strip():
			words.append(l.strip().split('\t')[1].strip().replace(' ','_'))
	writer.write(' '.join(words)+'\n')

writer.flush()
writer.close()