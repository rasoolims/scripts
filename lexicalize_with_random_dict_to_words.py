import os,sys,codecs,random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict

word_dict = defaultdict(list)

reader = codecs.open(os.path.abspath(sys.argv[2]),'r')
line = reader.readline()
while line:
	spl = line.strip().split()
	if len(spl)>1:
		word_dict[spl[0]].append(spl[1])
	line = reader.readline()

put_word = False if len(sys.argv)<5 or sys.argv[4]!='w' else True	


trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
writer = codecs.open(os.path.abspath(sys.argv[3]),'w')

for tree in trees:
	for i in range(0,len(tree.words)):
		tree.lemmas[i] = tree.words[i]
		
		if word_dict.has_key(tree.words[i]):
			tree.words[i] =  random.sample(word_dict[tree.words[i]],1)[0]
		elif tree.tags[i] == '.':
			tree.words[i] = tree.words[i]
		else:
			tree.words[i] = "_" if not put_word else tree.words[i]
		
	writer.write(tree.conll_str()+'\n\n')
writer.close()