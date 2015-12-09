import os,sys,codecs
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict

context_grams = defaultdict(list)

trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))

for tree in trees:
	t = ['<s>','<s>']+list(tree.tags)+['</s>','</s>']
	
	for i in range(0,len(tree.tags)):
		child_context = t[i+1]+' '+t[i+2]+' '+t[i+3]
		cw = tree.words[i]
		h = tree.heads[i]
		head_context = '_ ROOT _'
		hw = 'ROOT'
		if h>0:
			hw = tree.words[h-1]
			head_context = t[h]+' '+t[h+1]+' '+t[h+2]
		rel = tree.labels[i]

		context = rel +' '+child_context +' '+head_context


		words = cw+' '+hw
		context_grams[context].append(words)


writer = codecs.open(os.path.abspath(sys.argv[2]),'w')

for context in context_grams.keys():
	for words in context_grams[context]:
		writer.write(context+'\t'+words+'\n')

writer.close()