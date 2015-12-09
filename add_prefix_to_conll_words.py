import os,sys,codecs,random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict
from random import randint
tags = set(['.','ADJ','ADP','ADV','CONJ','DET','NOUN','NUM','PRON','PRT','VERB','X'])

words = set()
trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
prefix = sys.argv[2]
writer = codecs.open(sys.argv[3],'w')
for tree in trees:
	for i in range(0,len(tree.words)):
		if tree.tags[i]!='.':
			tree.words[i]= prefix+'_'+tree.words[i]
	writer.write(tree.conll_str()+'\n\n')

writer.close()