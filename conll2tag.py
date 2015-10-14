import os,sys,codecs

sens=codecs.open(os.path.abspath(sys.argv[1]),'r', encoding='utf-8').read().split('\n\n')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w', encoding='utf-8')
delim='_'

fp=3
if len(sys.argv)>3:
	if sys.argv[3]==u'fp':
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
				ws=l.strip().split('\t')[1].strip().split(' ')
				for w in ws:
					words.append(w+delim+(l.strip().split('\t')[fp].replace('_','-')))
			else:
				words.append(l.strip().split('\t')[1].strip()+delim+(l.strip().split('\t')[fp].replace('_','-')))
	writer.write(' '.join(words)+'\n')

writer.flush()
writer.close()