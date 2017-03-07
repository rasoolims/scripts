import sys,codecs,os

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')

delim='_'
if len(sys.argv)>3:
	delim=sys.argv[3]

line=reader.readline()
while line:
	spl=line.strip().split('\t')[0].split(' ')
	lab = line.strip().split('\t')[1]
	output=list()
	i=0
	for s in spl:
		if delim in s:
			i+=1
			word=s[:s.rfind(delim)]
			
			output.append(word)
	if i>0:
		writer.write(' '.join(output)+'\t'+lab+'\n')
	line=reader.readline()

writer.flush()
writer.close()