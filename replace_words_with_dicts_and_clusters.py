import os,sys,codecs,random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict

if len(sys.argv)<6:
	print 'tree_file dict_file target_word_list shared_cluster_file output_tree'

word_dict = defaultdict(str)

trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
reader = codecs.open(os.path.abspath(sys.argv[2]),'r')
line = reader.readline()
while line:
	spl = line.strip().split('\t')
	if len(spl)>1:
		word_dict[spl[0]]=spl[1]
	line = reader.readline()

target_words = set(codecs.open(os.path.abspath(sys.argv[3]),'r').read().strip().split('\n'))
shared_clusters = defaultdict()
target_shared_clusters = defaultdict(list)

cluster_reader = codecs.open(os.path.abspath(sys.argv[4]),'r')
line = cluster_reader.readline()
while line:
	spl = line.strip().split()
	if len(spl)>1:
		cls = spl[0]
		word = spl[1]
		shared_clusters[word] = cls
		if word in target_words:
			target_shared_clusters[cls].append(word)
	line = cluster_reader.readline()

writer = codecs.open(os.path.abspath(sys.argv[5]),'w')

for tree in trees:
	for i in range(0,len(tree.words)):
		tree.lemmas[i] = tree.words[i]
		if word_dict.has_key(tree.words[i].lower()):
			tree.words[i] = word_dict[tree.words[i].lower()]
		else:
			if shared_clusters.has_key(tree.words[i]):
				cls = shared_clusters[tree.words[i]]
				cands = target_shared_clusters[cls]

				if len(cands)>0:
					r = random.randint(0,len(cands)-1)
					tree.words[i] = cands[r]
				else:
					tree.words[i] = "_"

			else:
				tree.words[i] = "_"
		
	writer.write(tree.conll_str()+'\n\n')
writer.close()