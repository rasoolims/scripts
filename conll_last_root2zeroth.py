import os,codecs,sys

sentences=list()
reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')
lines=list()
line=reader.readline()
i=0
while line:
	line=line.strip()
	if line:
		lines.append(line)
	else:
		ln=len(lines)
		new_sen=list()
		for line in lines:
			spl=line.split('\t')
			if int(spl[6])==ln+1:
				spl[6]='0'
			new_sen.append('\t'.join(spl))
		writer.write('\n'.join(new_sen)+'\n\n')

		lines=list()
		i+=1
		if i%10000==0:
			sys.stdout.write(str(i)+'...')
			sys.stdout.flush()
	
	line=reader.readline()

sys.stdout.write('\n')

writer.flush()
writer.close()