# coding: utf8
import os,sys,codecs

sens=codecs.open(os.path.abspath(sys.argv[1]),'r').read().split('\n\n')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')
randomPar = False
if len(sys.argv)>3 and sys.argv[3]=='true':
	randomPar = True


i = 0
for sen in sens:
	lines=sen.strip().split('\n')
	
	words=list()
	for l in lines:
		if l.strip():
			spl =l.strip().split('\t')
			if spl[3] == 'PUNCT': 
				words.append('___')
			words.append(spl[1].strip())

	writer.write(' '.join(words).replace(' ___ ','').replace('___ ','').replace('___' ,'').replace('« ' ,' «').replace('[ ' ,' [').replace('( ' ,' (').replace('(. ' ,' (.').replace('(; ' ,' (;')+'\n')

	i+=1
	if randomPar and i%10==0:
		writer.write('\n')
writer.flush()
writer.close()

