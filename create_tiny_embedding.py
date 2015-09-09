import os,sys,codecs

print 'reading words'
words=set(codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n'))
words.add('*UNKNOWN*')
reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
writer=codecs.open(os.path.abspath(sys.argv[3]),'w')
print 'reading embeddings'

line=reader.readline()
while line:
	word=line.strip().split()[0]
	if word in words:
		writer.write(line.strip()+'\n')
	line=reader.readline()
writer.close()