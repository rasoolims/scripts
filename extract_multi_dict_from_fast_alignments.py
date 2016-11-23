import os,sys,codecs
from collections import defaultdict

src2trg_dict = defaultdict(lambda : defaultdict(int))

r1 = codecs.open(os.path.abspath(sys.argv[1]),'r')
r2 = codecs.open(os.path.abspath(sys.argv[2]),'r')
l1 = r1.readline()
while l1:
	src,trg = l1.strip().split('|||')
	alignments = r2.readline().strip().split()
	src_words = src.strip().split()
	trg_words = trg.strip().split()

	for align in alignments:
		a,b = align.split('-')
		src2trg_dict[src_words[int(a)]][trg_words[int(b)]]+=1

	l1 = r1.readline()

writer = codecs.open(os.path.abspath(sys.argv[3]),'w')

for s in src2trg_dict.keys():
	for t in src2trg_dict[s].keys():
		if src2trg_dict[s][t]>=5:
			writer.write(s+' '+t+' '+str(src2trg_dict[s][t])+'\n')
writer.close()