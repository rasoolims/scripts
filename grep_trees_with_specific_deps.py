import os,sys,codecs, operator
from collections import defaultdict
from mst_dep_tree_loader import DependencyTree

if len(sys.argv)<4:
	print 'input_file deps(separated by ,) output_file'

print 'reading trees'
t = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')
dependencies = set(sys.argv[3].strip().split(','))
head_pos = set(sys.argv[4].strip().split(',')) if len(sys.argv)>4 else set()

print 'writing trees'
seen = 0
for tree in t:
	seen_labels = set()

	for i in xrange(len(tree.labels)):
		if tree.labels[i] in dependencies:
			if len(head_pos)==0 or tree.tags[tree.heads[i]-1] in head_pos:
				seen_labels.add(tree.labels[i])
	if len(dependencies) == len(seen_labels):
		writer.write(tree.conll_str()+'\n\n')
		seen+=1
writer.close()
print 'num of seen',seen,'out of',len(t)
