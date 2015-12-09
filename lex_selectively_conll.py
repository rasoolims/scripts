
import os,sys,codecs,random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict
from random import randint
tags = set(['.','ADJ','ADP','ADV','CONJ','DET','NOUN','NUM','PRON','PRT','VERB','X'])

words = set()
lexicalized_trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
for tree in lexicalized_trees:
	for i in range(0,len(tree.words)):
		t_b2 = '<s>' if i<2 else tree.tags[i-2]
		t_b1 = '<s>' if i<1 else tree.tags[i-1]
		t_a1 = '</s>' if i>len(tree.words)-2 else  tree.tags[i+1]
		t_a2 = '</s>' if i>len(tree.words)-3 else  tree.tags[i+2]
		word = tree.words[i]
		if not word in tags:
			context = t_b2+' '+t_b1+' '+word+' '+t_a1+' '+t_a2
			words.add(context)
print len(words)

writer = codecs.open(os.path.abspath(sys.argv[3]),'w')
target_trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[2]))
for tree in target_trees:
	for i in range(0,len(tree.words)):
		t_b2 = '<s>' if i<2 else tree.tags[i-2]
		t_b1 = '<s>' if i<1 else tree.tags[i-1]
		t_a1 = '</s>' if i>len(tree.words)-2 else  tree.tags[i+1]
		t_a2 = '</s>' if i>len(tree.words)-3 else  tree.tags[i+2]
		word = tree.words[i]
		context = t_b2+' '+t_b1+' '+word+' '+t_a1+' '+t_a2

		if tree.tags[i]=='.' and len(tree.words)<=2:
			tree.words[i]=tree.words[i]
		elif not context in words:
			tree.words[i] = tree.tags[i]
	writer.write(tree.conll_str()+'\n\n')
writer.close()
