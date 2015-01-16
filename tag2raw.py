import sys,codecs,os

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')

line=reader.readline()
while line:
	spl=line.strip().split(' ')
	output=list()
	i=0
	for s in spl:
		if '_' in s:
			i+=1
			word=s[:s.rfind('_')]
			
			output.append(word)
	if i>0:
		writer.write(' '.join(output)+'\n')
	line=reader.readline()

writer.flush()
writer.close()