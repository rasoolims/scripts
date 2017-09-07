import os,sys,codecs


reader = codecs.open(os.path.abspath(sys.argv[1]),'r')
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')

sent = []
for line in reader:
	spl = line.strip().split()
	if len(spl)>=3:
		sent.append(spl[0]+'_'+spl[1])
	else:
		writer.write(' '.join(sent)+'\n')
		sent = []
writer.close()
