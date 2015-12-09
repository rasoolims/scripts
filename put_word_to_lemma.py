import os,sys,codecs,random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict

word_dict = defaultdict(str)


trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')

for tree in trees:
	for i in range(0,len(tree.words)):
		tree.lemmas[i] = tree.words[i]
		tree.words[i] = tree.words[i]
	writer.write(tree.conll_str()+'\n\n')
writer.close()