import os,sys,codecs,operator

lines = codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n')

words = set()
for l in lines:
	for i in l.strip().split(' '):
		words.add(i) 

embed_reader =  codecs.open(os.path.abspath(sys.argv[2]),'r')
embed_writer =  codecs.open(os.path.abspath(sys.argv[3]),'w')

line = embed_reader.readline()
c = 0
f = 0
while line:
	w = line.strip().split(' ')[0]
	if w in words or w.lower() in words:
		embed_writer.write(line.strip()+'\n')
	else: f+=1
	c+= 1
	if c%100000 ==0:
		sys.stdout.write(str(c)+'/'+str(f)+'...')
	line = embed_reader.readline()

embed_writer.flush()
embed_writer.close()
print 'done!'