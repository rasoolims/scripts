import os,sys,codecs,random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict

word_dict = defaultdict(str)

reader = codecs.open(os.path.abspath(sys.argv[2]),'r')
line = reader.readline()
while line:
	spl = line.strip().split('\t')
	if len(spl)>1:
		word_dict[spl[0]]=spl[1]

	line = reader.readline()


trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
writer = codecs.open(os.path.abspath(sys.argv[3]),'w')

for tree in trees:
	for i in range(0,len(tree.words)):
		if word_dict.has_key(tree.words[i].lower()):
			tree.lemmas[i] = word_dict[tree.words[i].lower()]
		else:
			tree.lemmas[i] = '_'
	writer.write(tree.conll_str()+'\n\n')
writer.close()