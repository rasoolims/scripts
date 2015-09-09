import os,sys,codecs

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')
line=reader.readline()
while line:
	spl=line.strip().split(' ')

	output1=list()
	output2=list()
	output3=list()
	output4=list()
	for s in spl:
		x=s.rfind('_')
		word=s[:x]
		tag=s[x+1:]

		output1.append(word)
		output2.append(tag)
		output3.append('_')
		output4.append('-1')

	writer.write('\t'.join(output1)+'\n')
	writer.write('\t'.join(output2)+'\n')
	writer.write('\t'.join(output3)+'\n')
	writer.write('\t'.join(output4)+'\n\n')


	line=reader.readline()

writer.close()