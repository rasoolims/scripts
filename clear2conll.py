import os,sys,codecs

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')
line=reader.readline()
while line:
	line=line.strip()

	if line:
		spl=line.split('\t')
		spl[3]=spl[4]
		output=spl[0]+'\t'+spl[1]+'\t_\t'+spl[4]+'\t_\t_\t'+spl[9]+'\t'+spl[11]+'\t_\t_'
		writer.write(output+'\n')
	else:
		writer.write('\n')

	line=reader.readline()
writer.flush()
writer.close()