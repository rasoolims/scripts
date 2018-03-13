import os,sys,codecs,random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict
from random import randint


trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
langs = set(sys.argv[2].strip().split(','))
writer = codecs.open(os.path.abspath(sys.argv[3]), 'w')

for tree in trees:
	if tree.lang_id in langs:
		writer.write(tree.conll_str()+'\n\n')
writer.close()