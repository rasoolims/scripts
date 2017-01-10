import os,sys,codecs
from collections import defaultdict

r1 = codecs.open(os.path.abspath(sys.argv[1]),'r')
r2 = codecs.open(os.path.abspath(sys.argv[2]),'r')
ar = codecs.open(os.path.abspath(sys.argv[3]),'r')
w = codecs.open(os.path.abspath(sys.argv[4]),'w')

l1 = r1.readline().strip()
while l1:
	dst_words = r2.readline().strip().lower().split()
	alignments = dict()
	for a in ar.readline().strip().split():
		s,t = a.strip().split('-')
		alignments[int(s)] = int(t)

	src_words = []
	src_tags = []
	
	for wt in l1.split():
		i = wt.rfind('_')
		src_words.append(wt[:i].lower())
		src_tags.append(wt[i+1:])

	output = []
	for i in xrange(len(src_words)):
		o = src_words[i]+' '+src_tags[i]+' '+ (dst_words[alignments[i]] if i in alignments else '_')
		output.append(o)

	w.write('\n'.join(output)+'\n\n')

	l1 = r1.readline().strip()

w.close()
