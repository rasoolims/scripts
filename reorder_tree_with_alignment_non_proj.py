import os,sys,codecs,random,operator,math
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict


def reorder(line, source_words):
	a = defaultdict(list)
	for spl in line.strip().split(' '):
		s,t = spl.split('-')
		s,t = int(s), int(t)
		a[s].append(t)


	swl = dict()
	sa = sorted(a.items(), key=operator.itemgetter(0))
	v, sv = set(), set()
	ordered = []
	for a in sa:
		for m in sorted(a[1]):
			if not m in v:
				ordered.append(m)
				if not a[0] in sv:
					if a[0] > 0:
						swl[m] = source_words[a[0]- 1] 
						sv.add(a[0])
			v.add(m)
	return ordered, swl

def eligible(j, v, absent):
	if not (j in  absent):
		return False
	for m in range(1, j):
		if m in v:
			return False
	return True

def fix_missing_items(o, target_len):
	v = set(o)
	absent = set()
	for i in range(target_len+1):
		if not i in v:
			absent.add(i)

	v.remove(o[0])
	new_order = [0]
	for i in o[1:]:
		v.remove(i)
		for j in range(0, i):
			if eligible(j, v, absent):
				new_order.append(j)
				absent.remove(j)
		new_order.append(i)
	for j in range(0, target_len+1):
		if j in absent:
			new_order.append(j)
			absent.remove(j)
	return new_order


target_trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
source_trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[2]))
alignments = codecs.open(os.path.abspath(sys.argv[3]), 'r').read().strip().split('\n')
writer = codecs.open(os.path.abspath(sys.argv[4]), 'w')
word_writer = codecs.open(os.path.abspath(sys.argv[5]), 'w')
log_writer = codecs.open(os.path.abspath(sys.argv[5])+'.log', 'w')
print os.path.abspath(sys.argv[5])+'.log'


assert len(target_trees)==len(alignments)
print len(target_trees), len(source_trees),len(alignments)

less_non_proj, just_two_most_proj = 0, 0
less_non_proj_better, just_two_most_proj_better = 0, 0

for i in range(len(target_trees)):
	target_words = target_trees[i].words
	target_len = len(target_words)
	new_order, swl = reorder(alignments[i], source_trees[i].words)
	if target_len != len(new_order) -1:
		new_order = fix_missing_items(new_order, target_len)
	source_words = []
	for no in new_order[1:]:
		if no in swl:
			source_words.append(swl[no])
		else:
			source_words.append('<unk>')

	assert target_len == len(new_order) -1
	new_tree = target_trees[i].reorder_with_order(new_order[1:])
	
	# log_writer.write('>>>>\n')
	# log_writer.write(alignments[i].strip()+'\n')
	# log_writer.write(' '.join(source_trees[i].words)+'\n')
	# log_writer.write(' '.join(target_trees[i].words) + '\n')
	# log_writer.write(' '.join([target_words[o-1] for o in new_order[1:]]) + '\n')
	orig_non_proj = len(DependencyTree.get_nonprojective_arcs(target_trees[i].heads))
	new_non_proj = len(DependencyTree.get_nonprojective_arcs(new_tree.heads))

	if new_non_proj <= orig_non_proj:
		less_non_proj += 1


	if new_non_proj <= orig_non_proj + 1:
		just_two_most_proj += 1
		writer.write(' '.join([str(o) for o in new_order[1:]]) + '\n')
		target_tags = target_trees[i].tags
		word_writer.write(' '.join([target_words[ti]+'_'+target_tags[ti] for ti in range(len(target_words))]) + '\n')
		log_writer.write(str(orig_non_proj) + '->'+ str(new_non_proj)+ '\n')
		log_writer.write(target_trees[i].conll_str() + '\n\n')
		log_writer.write(new_tree.conll_str() + '\n\n')
		log_writer.write('>>>>>>>>>>>>\n')



log_writer.close()
writer.close()
print len(target_trees)
print less_non_proj, just_two_most_proj
