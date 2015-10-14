import os,sys,codecs
from collections import defaultdict
from mst_dep_tree_loader import DependencyTree

writer = codecs.open(sys.argv[4],'w')
vote_3_trees = DependencyTree.load_trees_from_file(os.path.abspath(sys.argv[3]))
vote_2_trees = DependencyTree.load_trees_from_file(os.path.abspath(sys.argv[2]))
vote_1_trees = DependencyTree.load_trees_from_file(os.path.abspath(sys.argv[1]))

tree_dic = defaultdict()

for tree in vote_1_trees:
	tree_dic[' '.join(tree.words)] = tree

for tree in vote_2_trees:
	tree_dic[' '.join(tree.words)] = tree

for tree in vote_2_trees:
	tree_dic[' '.join(tree.words)] = tree


for tree in tree_dic.values():
	writer.write(tree.strip()+'\n\n')
writer.close() 
