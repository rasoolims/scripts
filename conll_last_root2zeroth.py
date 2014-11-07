import os,codecs,sys

sentences=codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')

for sentence in sentences:
	lines=sentence.strip().split('\n')
	ln=len(lines)
	new_sen=list()
	for line in lines:
		spl=line.split('\t')
		if int(spl[6])==ln+1:
			spl[6]='0'

		new_sen.append('\t'.join(spl))

	writer.write('\n'.join(new_sen)+'\n\n')

writer.flush()
writer.close()