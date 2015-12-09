import os,sys,codecs,random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict
from random import randint

if len(sys.argv)<3:
	print '[list of conll files + weight] output_file'
	sys.exit(0)


print 'reading trees'
all_trees = list()
for i in range(1,len(sys.argv)-1,2):
	trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[i]))
	weight = int(sys.argv[i+1])

	for w in range(0,weight):
		all_trees = all_trees + trees

print 'shuffling trees'
lst = range(0,len(all_trees))
random.shuffle(lst)

print 'writing trees'
writer = codecs.open(os.path.abspath(sys.argv[-1]),'w')
for l in lst:
	writer.write(all_trees[l].conll_str()+'\n\n')
writer.close()
