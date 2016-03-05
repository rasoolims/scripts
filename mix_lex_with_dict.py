import os,sys,codecs,random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict
from random import randint

print 'reading dict'
dictionary = dict()
reader = codecs.open(os.path.abspath(sys.argv[1]),'r')
line = reader.readline()
while line:
	spl = line.strip().split('\t')
	if len(spl)==2:
		dictionary[spl[0]] = spl[1]
	line = reader.readline()

print 'reading file..'
reader = codecs.open(os.path.abspath(sys.argv[2]),'r')
line = reader.readline()
writer = codecs.open(os.path.abspath(sys.argv[3]),'w')
while line:
	spl = line.strip().split(' ')
	has_context = False
	for i in range(0, len(spl)):
		if dictionary.has_key(spl[i]):
			has_context = True
			spl[i] = dictionary[spl[i]]
	if has_context:
		writer.write(' '.join(spl)+'\n')
	line = reader.readline()
writer.close()