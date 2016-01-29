import os,sys,codecs

reader1=codecs.open(os.path.abspath(sys.argv[1]),'r')
langId = sys.argv[2]
writer1=codecs.open(os.path.abspath(sys.argv[3]),'w')


line1=reader1.readline()

while line1:
	spl=line1.strip().split('\t')
	if len(spl)>2:
		spl[1] = spl[1].lower()
		writer1.write('\t'.join(spl)+'\n')
	else:
		writer1.write(line1)

	line1=reader1.readline()
writer1.close()