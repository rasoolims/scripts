import os,sys,codecs

sens=codecs.open(os.path.abspath(sys.argv[1]),'r').read().split('\n\n')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')
delim='_'

fp=3
if len(sys.argv)>3:
	if sys.argv[3]=='fp':
		fp=4
	else:
		delim=sys.argv[3]


for sen in sens:
	lines=sen.strip().split('\n')
	words=list()
	for l in lines:
		if l.strip():
			if ' ' in l.strip().split('\t')[1].strip():
				print l.strip().split('\t')[1].strip()
				print l
			words.append(l.strip().split('\t')[1].strip()+delim+(l.strip().split('\t')[fp].replace('_','-')))
	writer.write(' '.join(words)+'\n')

writer.flush()
writer.close()