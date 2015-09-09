import os,sys,codecs

reader1=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer1=codecs.open(os.path.abspath(sys.argv[2]),'w')

line1=reader1.readline()

while line1:
	spl=line1.strip().split('\t')
	if len(spl)>2:
		spl[3]='_'
		spl[4]='_'
		writer1.write('\t'.join(spl)+'\n')
	else:
		writer1.write(line1)

	line1=reader1.readline()
writer1.close()