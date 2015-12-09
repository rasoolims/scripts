import os,sys,codecs,random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict

trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
word_dict = defaultdict(set)


for tree in trees:
	for word in tree.words:
		word_dict[tree.lang_id].add(word.lower())


writer = codecs.open(os.path.abspath(sys.argv[2]),'w')
for lang in word_dict.keys():
	for word in word_dict[lang]:
		writer.write(lang+'\t'+word+'\n')
writer.close()
