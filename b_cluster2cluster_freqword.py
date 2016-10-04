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
	spl = line.strip().split('\t')
	if len(spl)>=2:
		if not spl[1] in frequent_words:
			spl[0] = 'cluster_cls_'+spl[0]
		else:
			spl[0] = spl[1]
		out = spl[1]+' '+spl[0]+'\n'
		writer.write(out)
	line = reader.readline()
writer.close()