import os,sys,codecs

reader1 = codecs.open(os.path.abspath(sys.argv[1]),'r')
langId = sys.argv[2]
writer1 = codecs.open(os.path.abspath(sys.argv[3]),'w')


line1=reader1.readline()

while line1:
	if len(line1.strip())==0:
		writer1.write(line1)
	else:
		spl=line1.strip().split('\t')
		if len(spl)>2:
			if not '-' in spl[0]:
				spl[5] = langId
				if ':' in spl[7]:
					spl[7] = spl[7][:spl[7].rfind(':')]
				writer1.write('\t'.join(spl)+'\n')
	

	line1=reader1.readline()
writer1.close()