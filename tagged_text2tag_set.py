import os,sys,codecs,math
from collections import defaultdict

tagset = defaultdict(set)

r1 = codecs.open(os.path.abspath(sys.argv[1]),'r')
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')
l1 = r1.readline()

while l1:
	for w_t in l1.strip().split():
		i = w_t.rfind('_')
		w = w_t[:i]
		t = w_t[i+1:]
		tagset[w].add(t)
	l1 = r1.readline()

for w in tagset.keys():
	output = w+ '\t' +' '.join([y for y in tagset[w]])+'\n'
	writer.write(output)
writer.close()