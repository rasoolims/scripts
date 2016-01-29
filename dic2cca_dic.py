import os,sys,codecs

reader = codecs.open(os.path.abspath(sys.argv[1]),'r')
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')

line = reader.readline()
while line:
	spl = line.strip().split()
	if len(spl)>=2:
		writer.write(spl[0]+' ||| '+spl[1]+'\n')
	line = reader.readline()
writer.close()