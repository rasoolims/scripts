import os,sys,codecs,random,operator,math
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict

def score_tree(tree, dependency_dirs, pos_directions):
	a, a_ = 0, 0
	for i, h in enumerate(tree.heads):
		label = tree.labels[i]
		head_pos = tree.tags[h-1] if h>0 else 'ROOT' 
		dep_pos = tree.tags[i]
		pos_match =  dep_pos + '-'+ head_pos

		direction = 1 if h>i+1 else 0
		if label in dependency_dirs:
			a += dependency_dirs[label][direction]
			a_ += 1
		#else:
			#a += def_log
		if pos_match in pos_directions:
			a += pos_directions[pos_match][direction]
			a_ += 1
	return a


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

gold_treebank = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))

dependency_dirs,pos_directions = dict(), dict()
for tree in gold_treebank:
	for i, h in enumerate(tree.heads):
		label = tree.labels[i]
		head_pos = tree.tags[h-1] if h>0 else 'ROOT' 
		dep_pos = tree.tags[i]
		pos_match =  dep_pos + '-'+ head_pos

		if not label in dependency_dirs:
			dependency_dirs[label] = [0, 0]
		direction = 1 if h>i+1 else 0
		dependency_dirs[label][direction] += 1

		if not pos_match in pos_directions:
			pos_directions[pos_match] = [0, 0]
		pos_directions[pos_match][direction] += 1

for label in dependency_dirs.keys():
	all_ = dependency_dirs[label][0] + dependency_dirs[label][1]
	dependency_dirs[label][0] = float(dependency_dirs[label][0])/all_
	dependency_dirs[label][1] = float(dependency_dirs[label][1])/all_
	if dependency_dirs[label][0] > 0.75:
		dependency_dirs[label][0] = 1
		dependency_dirs[label][1] = -1
	elif dependency_dirs[label][1] > 0.75:
		dependency_dirs[label][0] = -1
		dependency_dirs[label][1] = 1
	else:
		dependency_dirs[label][1] = 0
		dependency_dirs[label][0] = 0

	print label, dependency_dirs[label]

for label in pos_directions.keys():
	all_ = pos_directions[label][0] + pos_directions[label][1]
	pos_directions[label][0] = float(pos_directions[label][0])/all_
	pos_directions[label][1] = float(pos_directions[label][1])/all_
	if pos_directions[label][0] > 0.75:
		pos_directions[label][0] = 1
		pos_directions[label][1] = -1
	elif pos_directions[label][1] > 0.75:
		pos_directions[label][0] = -1
		pos_directions[label][1] = 1
	else:
		pos_directions[label][1] = 0
		pos_directions[label][0] = 0
	print label, pos_directions[label]

target_trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[2]))
source_trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[3]))
alignments = codecs.open(os.path.abspath(sys.argv[4]), 'r').read().strip().split('\n')
writer = codecs.open(os.path.abspath(sys.argv[6]), 'w')
word_writer = codecs.open(os.path.abspath(sys.argv[7]), 'w')
orig_word_writer = codecs.open(os.path.abspath(sys.argv[7])+'.orig_words', 'w')
complex_writer = codecs.open(os.path.abspath(sys.argv[7])+'.complex', 'w')
complex_output_writer = codecs.open(os.path.abspath(sys.argv[6])+'.complex', 'w')

log_writer = codecs.open(os.path.abspath(sys.argv[7])+'.log', 'w')
print os.path.abspath(sys.argv[7])+'.log'

rec = codecs.open(sys.argv[5],'r').read().strip().split('\n')
dictionaries = dict()
for r in rec:
	spl = r.split('\t')
	dictionaries[spl[0]] = spl[1]

source_lang = sys.argv[2][:-6]
source_lang = source_lang[source_lang.rfind('.')+1:]

assert len(target_trees)==len(alignments)
print len(target_trees), len(source_trees),len(alignments)

better = 0
less_non_proj, just_two_most_proj = 0, 0
less_non_proj_better, just_two_most_proj_better = 0, 0

for i in range(len(target_trees)):
	target_words = target_trees[i].words
	if float(len(alignments[i].split()) - 1)/len(target_words) < 0.3:
		continue
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
	orig_score = score_tree(target_trees[i], dependency_dirs, pos_directions)
	new_tree = target_trees[i].reorder_with_order(new_order[1:])
	
	# log_writer.write('>>>>\n')
	# log_writer.write(alignments[i].strip()+'\n')
	# log_writer.write(' '.join(source_trees[i].words)+'\n')
	# log_writer.write(' '.join(target_trees[i].words) + '\n')
	# log_writer.write(' '.join([target_words[o-1] for o in new_order[1:]]) + '\n')
	score = score_tree(new_tree, dependency_dirs, pos_directions)
	orig_non_proj = len(DependencyTree.get_nonprojective_arcs(target_trees[i].heads))
	new_non_proj = len(DependencyTree.get_nonprojective_arcs(new_tree.heads))
	if score>orig_score:
		better += 1
	if new_non_proj <= orig_non_proj:
		less_non_proj += 1
		if score>=orig_score:
			less_non_proj_better += 1


	if new_non_proj <= orig_non_proj + 2:
		just_two_most_proj += 1
		if score>=orig_score:
			just_two_most_proj_better += 1

			writer.write(' '.join([str(o) for o in new_order[1:]]) + '\n')
			target_tags = target_trees[i].tags
			translated_words = [dictionaries[target_words[ti]] if target_words[ti] in dictionaries else target_words[ti] for ti in range(len(target_words))]
			relation = [target_trees[i].labels[ti] + ('-left' if target_trees[i].heads[ti]>=ti else '-right') for ti in range(len(target_words))]
			word_writer.write(' '.join([translated_words[ti]+'_'+target_tags[ti] for ti in range(len(target_words))]) + '\n')
			complex_writer.write(' '.join([translated_words[ti]+'_'+target_tags[ti]+'_'+relation[ti]+'_'+source_lang for ti in range(len(target_words))]) + '\n')
			orig_word_writer.write(' '.join([target_words[ti]+'_'+target_tags[ti] for ti in range(len(target_words))]) + '\n')
			#log_writer.write(str(orig_non_proj) + '->'+ str(new_non_proj)+ '\n')
			
			rev_relation = [new_tree.labels[ti] + ('-left' if new_tree.heads[ti]>=ti else '-right') for ti in range(len(target_words))]
			complex_output_writer.write(' '.join([new_tree.words[ti]+'_'+new_tree.tags[ti]+'_'+rev_relation[ti] for ti in range(len(target_words))]) + '\n')
			log_writer.write(str(orig_score) +'->'+ str(score)+ '\n')
			log_writer.write(alignments[i]+'\n\n')
			log_writer.write(target_trees[i].conll_str() + '\n\n')
			log_writer.write(new_tree.conll_str() + '\n\n')
			log_writer.write('>>>>>>>>>>>>\n')



log_writer.close()
writer.close()
word_writer.close()
complex_output_writer.close()
complex_writer.close()
print better, len(target_trees)
print less_non_proj, just_two_most_proj
print less_non_proj_better, just_two_most_proj_better