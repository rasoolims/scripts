import os,sys,codecs
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict

trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')

for tree in trees:
	t = ['<s>','<s>']+list(tree.tags)+['</s>','</s>']
	for i in range(3,len(t)-1):
		unigram_context = ' '.join(t[i-3:i+2])
		writer.write('unigram\t'+unigram_context+'\t'+tree.words[i-3]+'\n')

writer.close()