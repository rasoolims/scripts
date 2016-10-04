import os,sys,codecs,operator
from collections import defaultdict

clusters =  defaultdict(int)

print 'reading freq words'
frequent_words = set(codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n'))

print 'reading dics'
reader = codecs.open(os.path.abspath(sys.argv[2]),'r')
line = reader.readline()
while line:
	spl = line.strip().split(' ')
	if len(spl)==2:
		clusters[spl[0]] = int(spl[1])
	line = reader.readline()

c = 0
print 'writing new words'
reader = codecs.open(os.path.abspath(sys.argv[3]),'r')
writer = codecs.open(os.path.abspath(sys.argv[4]),'w')
line = reader.readline()
while line:
	spl = line.strip().split(' ')
	for i in range(0,len(spl)):
		w = spl[i]
		if not w in frequent_words:
			if clusters.has_key(w):
				spl[i] = 'cluster_'+str(clusters[w])
			else:
				spl[i] = '_unk_'
	c+= 1
	if c%100000==0:
		sys.stdout.write(str(c)+'...')
	writer.write(' '.join(spl)+'\n')
	line = reader.readline()
writer.close()
sys.stdout.write(str(c)+'...done!\n')


