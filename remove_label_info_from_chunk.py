import os,sys,codecs

reader = codecs.open(os.path.abspath(sys.argv[1]),'r')
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')

for line in reader:
	spl = line.strip().split()
	if len(spl)>=3:
		if '-' in spl[2]:
			spl[2]=spl[2][:1]+'-L'
		if len(spl)>3:
			if '-' in spl[3]:
				spl[3]=spl[3][:1]+'-L'
		writer.write(' '.join(spl)+'\n')
	else:
		writer.write(line.strip()+'\n')
writer.close()
