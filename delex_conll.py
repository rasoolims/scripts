import os,sys,codecs

reader1=codecs.open(os.path.abspath(sys.argv[1]),'r')
langId = sys.argv[2]
writer1=codecs.open(os.path.abspath(sys.argv[3]),'w')

tags = set(['.','ADJ','ADP','ADV','CONJ','DET','NOUN','NUM','PRON','PRT','VERB','X'])

line1=reader1.readline()

while line1:
	spl=line1.strip().split('\t')
	if len(spl)>2:
		#if not spl[3] in tags and spl[1] in tags:
		#	tmp = spl[3]
		#	spl[3] = spl[1]
		#	spl[2]= spl[1]
		#	spl[1]=tmp
		#	spl[2]='_'
		#else:
		spl[2]=spl[1]
		spl[1]='_'

		if spl[1]=='.' and len(spl[2])<=2:
			spl[1] = spl[2]
		if langId!='_':
			spl[5] = langId
		writer1.write('\t'.join(spl)+'\n')
	else:
		writer1.write(line1)

	line1=reader1.readline()
writer1.close()