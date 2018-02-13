import os,sys,codecs,random,operator,math
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict

def reorder(line):
	a = defaultdict(list)
	for spl in line.strip().split(' '):
		s,t = spl.split('-')
		s,t = int(s), int(t)
		a[s].append(t)

	sa = sorted(a.items(), key=operator.itemgetter(0))
	v = set()
	ordered = []
	for a in sa:
		for m in sorted(a[1]):
			if not m in v:
				ordered.append(m)
			v.add(m)
	return ordered

def fix_missing_items(o, target_len):
	v = set(o)
	absent = set()
	for i in range(target_len+1):
		if not i in v:
			absent.add(i)

	new_order = [0]
	for i in o[1:]:
		for j in range(0, i):
			if j in absent:
				new_order.append(j)
				absent.remove(j)
		new_order.append(i)
	for j in range(0, target_len+1):
		if j in absent:
			new_order.append(j)
			absent.remove(j)
	return new_order

target_text = codecs.open(os.path.abspath(sys.argv[1]), 'r').read().strip().split('\n')
source_text = codecs.open(os.path.abspath(sys.argv[2]), 'r').read().strip().split('\n')
alignments = codecs.open(os.path.abspath(sys.argv[3]), 'r').read().strip().split('\n')
writer = codecs.open(os.path.abspath(sys.argv[4]), 'w')
word_writer = codecs.open(os.path.abspath(sys.argv[5]), 'w')
log_writer = codecs.open(os.path.abspath(sys.argv[5])+'.log', 'w')

assert len(target_text)==len(alignments)
for i in range(len(target_text)):
	target_words = target_text[i].strip().split()
	target_len = len(target_words)
	new_order = reorder(alignments[i])
	if target_len != len(new_order) -1:
		new_order = fix_missing_items(new_order, target_len)
	assert target_len == len(new_order) -1
	writer.write(' '.join([str(o) for o in new_order[1:]]) + '\n')
	log_writer.write('>>>>\n')
	log_writer.write(source_text[i].strip()+'\n')
	log_writer.write(target_text[i].strip() + '\n')
	log_writer.write(' '.join([target_words[o-1] for o in new_order[1:]]) + '\n')
	word_writer.write(' '.join([target_words[o-1] for o in new_order[1:]]) + '\n')
log_writer.close()
writer.close()
