from mst_dep_tree_loader import DependencyTree
import os, sys, operator
from collections import defaultdict

trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
tcount = defaultdict(int)
for t in trees:
	tcount[t.lang_id] += 1

st = sorted(tcount.items(), key=operator.itemgetter(1), reverse=True)
for l in st:
	print l[0], l[1]
