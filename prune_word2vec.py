import os,sys,codecs

words = set(codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n'))

writer = codecs.open(os.path.abspath(sys.argv[3]),'w')
for line in codecs.open(os.path.abspath(sys.argv[2]),'r'):
	word = line.split()[0]
	if word in words:
		writer.write(line.strip()+'\n')
writer.close()