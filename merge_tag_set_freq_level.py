import os,sys,codecs,pickle
from collections import defaultdict

freq_reader = codecs.open(os.path.abspath(sys.argv[1]),'r')
tagset_reader = codecs.open(os.path.abspath(sys.argv[2]),'r')

tags_dict = defaultdict(set)
freq_dict = dict()

l1 = freq_reader.readline()
while l1: 
	w,l,f = l1.strip().split()
	freq_dict[w]= l
	l1 = freq_reader.readline()

l1 = tagset_reader.readline()
while l1: 
	w,ts = l1.strip().split('\t')
	[tags_dict[t].add(w) for t in ts.split()]
	l1 = tagset_reader.readline()

final_dict = defaultdict(set)

for t in tags_dict.keys():
	for w in tags_dict[t]:
		if w in freq_dict:
			l = freq_dict[w] + ' '+t
			final_dict[l].add(w)

f = codecs.open(os.path.abspath(sys.argv[3]),'wb')
pickle.dump(final_dict, f)
