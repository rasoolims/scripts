import os,sys,codecs,operator
from collections import defaultdict

clusters = dict()
frequent_words = set()

print 'reading dics'
reader = codecs.open(os.path.abspath(sys.argv[1]),'r')
frequent_words = set(codecs.open(os.path.abspath(sys.argv[2]),'r').read().strip().split('\n'))
writer = codecs.open(os.path.abspath(sys.argv[3]),'w')
line = reader.readline()
while line:
	spl = line.strip().split(' ')
	if len(spl)==2:
		if spl[0] in frequent_words:
			spl[1] = spl[0]
		else:
			spl[1] = 'cluster_'+spl[1]
		writer.write(' '.join(spl)+'\n')
	line = reader.readline()

writer.close()