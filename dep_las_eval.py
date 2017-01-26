import os,sys,codecs
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict

pt = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
gt = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[2]))

assert len(pt) == len(gt)

fp_h = defaultdict(int)
tp_h = defaultdict(int)
fn_h = defaultdict(int)

labels = set()
all_t = 0
for i in xrange(len(gt)):
	for j in xrange(len(gt[i].labels)):
		if gt[i].labels[j] == 'p' or gt[i].labels[j] == 'punct': continue
		all_t+=1
		g_h_l = gt[i].labels[j]
		p_h_l = pt[i].labels[j]
		if gt[i].heads[j]==pt[i].heads[j] and gt[i].heads[j]==pt[i].heads[j]:
			tp_h[g_h_l]+=1
		else:
			fp_h[p_h_l] += 1
			fn_h[g_h_l] += 1

		labels.add(g_h_l)
		labels.add(g_h_l)

for label in sorted(labels):
	precision = float(tp_h[label]*100)/(tp_h[label]+fp_h[label]) if tp_h[label]+fp_h[label]>0 else 0
	recall = float(tp_h[label]*100)/(tp_h[label]+fn_h[label]) if tp_h[label]+fn_h[label]>0 else 0
	f_score= float(2*precision*recall) /(precision+recall) if precision+recall>0 else 0
	head_count =  100*float(tp_h[label]+fn_h[label])/all_t
	print label,round(head_count,1),round(precision,1),round(recall,1),round(f_score,1)


