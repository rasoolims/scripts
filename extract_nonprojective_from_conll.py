import os,sys,codecs, operator
from collections import defaultdict
from mst_dep_tree_loader import DependencyTree

t = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')


print 'writing trees'
full = 0
for tree in t:
	if not DependencyTree.is_projective(tree.heads):
		writer.write(tree.conll_str()+'\n\n')
		full+=1
writer.close()
print 'num of full',full,'out of',len(t)
