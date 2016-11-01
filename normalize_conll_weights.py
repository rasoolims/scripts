import os,sys,codecs,random,math,operator
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict
from random import randint

if len(sys.argv)<4:
	print 'conll_file output_file max_num'
	sys.exit(0)


print 'reading target trees'

t = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))

min_score = float('inf')
max_score = float('-inf')

for tree in t:
	if tree.weight<min_score:
		min_score = tree.weight
	if tree.weight>max_score:
		max_score = tree.weight

print min_score, max_score

writer = codecs.open(os.path.abspath(sys.argv[2]), 'w')
for tree in t:
	tree.weight = (tree.weight- min_score)/(max_score - min_score)
	writer.write(tree.conll_str()+'\n\n')
writer.flush()
writer.close()
print 'done!'

