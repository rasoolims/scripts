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

target_text = codecs.open(os.path.abspath(sys.argv[1]), 'r').read().strip().split('\n')
source_text = codecs.open(os.path.abspath(sys.argv[2]), 'r').read().strip().split('\n')
alignments = codecs.open(os.path.abspath(sys.argv[3]), 'r').read().strip().split('\n')
writer = codecs.open(os.path.abspath(sys.argv[4]), 'w')
word_writer = codecs.open(os.path.abspath(sys.argv[5]), 'w')
log_writer = codecs.open(os.path.abspath(sys.argv[5])+'.log', 'w')
print os.path.abspath(sys.argv[5])+'.log'

assert len(target_text)==len(alignments)
for i in range(len(target_text)):
	target_words = target_text[i].strip().split()
	target_len = len(target_words)
	new_order, swl = reorder(alignments[i], source_text[i].strip().split())
	if target_len != len(new_order) -1:
		new_order = fix_missing_items(new_order, target_len)
	source_words = []
	for no in new_order[1:]:
		if no in swl:
			source_words.append(swl[no])
		else:
			source_words.append('<unk>')

	assert target_len == len(new_order) -1
	writer.write(' '.join([str(o) for o in new_order[1:]]) + '\n')
	log_writer.write('>>>>\n')
	log_writer.write(alignments[i].strip()+'\n')
	log_writer.write(source_text[i].strip()+'\n')
	log_writer.write(target_text[i].strip() + '\n')
	log_writer.write(' '.join([target_words[o-1] for o in new_order[1:]]) + '\n')
	word_writer.write(' '.join(source_words) + '\n')
log_writer.close()
writer.close()
