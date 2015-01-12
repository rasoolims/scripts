import sys,codecs,os

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')

line=reader.readline()
while line:
	spl=line.strip().split(' ')
	
	i=0
	for s in spl:
		if '_' in s:
			i+=1
			word=s[:s.rfind('_')]
			tag=s[s.rfind('_')+1:]
			output=str(i)+'\t'+word+'\t_\t'+tag+'\t_\t_\t0\t_\n'
			writer.write(output)
	if i>0:
		writer.write('\n')
	line=reader.readline()

writer.flush()
writer.close()