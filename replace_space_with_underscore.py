import sys,codecs,os

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')

line=reader.readline()
while line:
	line=line.strip().replace(' ','_')
	writer.write(line+'\n')
	line=reader.readline()

writer.flush()
writer.close()