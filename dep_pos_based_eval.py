import os,sys,codecs
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict

pt = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
gt = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[2]))

assert len(pt) == len(gt)

fp = defaultdict(int)
tp = defaultdict(int)

fp_h = defaultdict(int)
tp_h = defaultdict(int)
fn_h = defaultdict(int)

tags = set()
h_tags = set()
all_t = 0
for i in xrange(len(gt)):
	for j in xrange(len(gt[i].tags)):
		if gt[i].tags[j]=='PUNCT': continue
		all_t+=1
		tags.add(gt[i].tags[j])
		g_h_t = gt[i].tags[gt[i].heads[j]-1]
		p_h_t = gt[i].tags[pt[i].heads[j]-1]
		if gt[i].heads[j]==pt[i].heads[j]:
			tp[gt[i].tags[j]]+=1
			tp_h[g_h_t]+=1
		else:
			fp[gt[i].tags[j]]+=1
			fp_h[p_h_t] += 1
			fn_h[g_h_t] += 1

		h_tags.add(g_h_t)
		h_tags.add(p_h_t)

for tag in sorted(tags):
	precision = float(tp_h[tag]*100)/(tp_h[tag]+fp_h[tag]) if tp_h[tag]+fp_h[tag]>0 else 0
	recall = float(tp_h[tag]*100)/(tp_h[tag]+fn_h[tag]) if tp_h[tag]+fn_h[tag]>0 else 0
	f_score= float(2*precision*recall) /(precision+recall) if precision+recall>0 else 0
	dep_acc = float(tp[tag]*100)/(tp[tag]+fp[tag])
	dep_count  = 100*float(tp[tag]+fp[tag])/all_t
	head_count =  100*float(tp_h[tag]+fn_h[tag])/all_t
	print tag,round(dep_count,1), round(dep_acc,1), round(head_count,1),round(precision,1),round(recall,1),round(f_score,1)


