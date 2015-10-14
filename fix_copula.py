import os,sys,codecs
from collections import defaultdict
from termcolor import colored
from mst_dep_tree_loader import DependencyTree


if len(sys.argv)<3:
	print 'python fix_copula.py [input_path] [output_path]'

input_path = os.path.abspath(sys.argv[1])
output_path = os.path.abspath(sys.argv[2])

trees = DependencyTree.load_trees_from_file(input_path)

writer = codecs.open(output_path,'w')

for tree in trees:
	for i in range(0, len(tree.heads)):
		if tree.labels[i] == 'cop':
			print colored(tree.tree_str(), 'green')

			tree.flip_copula_head(tree.heads[i], i+1)

			print colored(tree.tree_str(), 'red')
			print '******'
	writer.write(tree.tree_str().strip()+'\n\n')

writer.close()