import os,sys,codecs

sens=codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')
max_len=int(sys.argv[3])

for sen in sens:
	if len(sen.strip().split('\n'))<max_len:
		writer.write(sen.strip()+'\n\n')

writer.close()