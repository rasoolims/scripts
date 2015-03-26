import os,sys,codecs

reader=codecs.open(sys.argv[1],'r')

dep=0
line=reader.readline()
while line:
	spl=line.strip().split('\t')
	if len(spl)>5:
		d=int(spl[6])
		if d!=-1:
			dep+=1
	line=reader.readline()

print dep