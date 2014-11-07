import os,sys,codecs

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')
line=reader.readline()
while line:
	line=line.strip()

	if line:
		spl=line.split('\t')
		del spl[4]
		writer.write('\t'.join(spl)+'\n')
	else:
		writer.write('\n')

	line=reader.readline()
writer.flush()
writer.close()