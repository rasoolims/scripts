import os,sys,codecs

lines=codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')

writer=codecs.open(os.path.abspath(sys.argv[2]),'w')
for l in lines:
	writer.write(' '.join(l.strip().split('\n'))+'\n')
writer.close()

