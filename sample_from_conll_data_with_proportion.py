import os,sys,codecs,random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict
from random import randint

if len(sys.argv)<4:
	print '[list of conll files + weight] output_file [max_num]'
	sys.exit(0)


print 'reading trees'
all_trees = list()
props = list()
for i in range(1,len(sys.argv)-2,2):
	t = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[i]))
	all_trees.append(t)
	weight = int(sys.argv[i+1])

	for w in range(0,weight):
		props.append(i)


print 'writing trees'
writer = codecs.open(os.path.abspath(sys.argv[-2]),'w')
for i in range(0, int(sys.argv[-1])):
	r = props[random.randint(0,len(props)-1)]
	t = all_trees[r][random.randint(0,len(all_trees[r])-1)]
	writer.write(t.conll_str()+'\n\n')

writer.close()
