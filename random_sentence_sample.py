import os,sys,codecs,random

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
ratio=float(sys.argv[2])
writer=codecs.open(os.path.abspath(sys.argv[3]),'w')

c=0
line=reader.readline()
while line:
	if random.random()<ratio:
		writer.write(line.strip()+'\n')
		c+=1
	line=reader.readline()
writer.flush()
writer.close()

print c
