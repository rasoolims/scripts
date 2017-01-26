# coding: utf8
import os,sys,codecs

sens=codecs.open(os.path.abspath(sys.argv[1]),'r').read().split('\n\n')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')

for sen in sens:
	lines=sen.strip().split('\n')
	
	words=list()
	for l in lines:
		if l.strip():
			spl =l.strip().split('\t')
			if spl[3] == 'PUNCT': 
				words.append('<SPLIT>')
			words.append(spl[1].strip())
			# if 'SpaceAfter=No' in spl[9]:
			# 	words.append('<SPLIT>')

	writer.write(' '.join(words).replace(' <SPLIT> ','<SPLIT>').replace(' <SPLIT> ','<SPLIT>').replace('<SPLIT> ','<SPLIT>').replace('<SPLIT> ','<SPLIT>').replace('«<SPLIT>' ,'<SPLIT>«').replace('[<SPLIT>' ,'<SPLIT>[').replace('(<SPLIT>' ,'<SPLIT>(').replace('(.<SPLIT>' ,'<SPLIT>(.').replace('(;<SPLIT>' ,'<SPLIT>(;').replace('<SPLIT><SPLIT>','<SPLIT>').replace('<SPLIT><SPLIT>','<SPLIT>')+'\n')

writer.flush()
writer.close()

