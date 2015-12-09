import sys,codecs,os

reader = codecs.open(os.path.abspath(sys.argv[1]),'r')
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')
sentences = set()
line = reader.readline()
while line:
	sentences.add(line.strip())
	line = reader.readline()
for sentence in sentences:
	writer.write(sentence+'\n')
writer.close()