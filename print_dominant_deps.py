import os,sys,codecs,random,operator,math
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict


gold_treebank = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
ignore_deps = set(['conj','cc','fixed','flat','compound','list','parataxis','orphan','goeswith','reparandum','punct','root','discourse','dep', '_','case','clf','det','mark'])

dependency_dirs,pos_directions = dict(), dict()
for tree in gold_treebank:
	for i, h in enumerate(tree.heads):
		label = tree.labels[i]
		if label in ignore_deps:
			continue
		head_pos = tree.tags[h-1] if h>0 else 'ROOT' 
		dep_pos = tree.tags[i]

		if not label in dependency_dirs:
			dependency_dirs[label] = [0, 0]
		direction = 1 if h>i+1 else 0
		dependency_dirs[label][direction] += 1

		

for label in dependency_dirs.keys():
	all_ = dependency_dirs[label][0] + dependency_dirs[label][1]
	dependency_dirs[label][0] = float(dependency_dirs[label][0])/all_
	dependency_dirs[label][1] = float(dependency_dirs[label][1])/all_
	if dependency_dirs[label][0] > 0.75:
		dependency_dirs[label][0] = 1
		dependency_dirs[label][1] = -1
		print label, 0
	elif dependency_dirs[label][1] > 0.75:
		dependency_dirs[label][0] = -1
		dependency_dirs[label][1] = 1
		print label, 1
	else:
		dependency_dirs[label][1] = 0
		dependency_dirs[label][0] = 0


