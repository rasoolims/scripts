import os,sys,codecs,random,operator,math
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict

ignore_deps = set(['conj','cc','fixed','flat','compound','list','parataxis','orphan','goeswith','reparandum','punct','root','discourse','dep', '_','case','clf','det','mark'])
skipped = 0
changed = 0

def same_dep_order(src_dep_order, dst_dep_order, label):
	if label in src_dep_order and label in dst_dep_order:
		if src_dep_order[label] == dst_dep_order[label]:
			return True
	return False

def score_tree(tree, dependency_dirs):
	a, a_ = 0, 0
	for i, h in enumerate(tree.heads):
		label = tree.labels[i]
		direction = 1 if h>i+1 else 0
		if label in dependency_dirs:
			a += dependency_dirs[label][direction]
			a_ += 1
	return a


def reorder(tree, head, dependency_dirs, src_dep_order):
	before_head = list()
	global skipped
	global changed
	after_head = list()
	current_order = []
	for dep in sorted(tree.reverse_tree[head]):
		label = tree.labels[dep-1]

		direction = 1 if head>dep else 0
		rev_direction = 1 if head<dep else 0

		orig_score, rev_score = 0, 0
		before = True if head>dep else 0
		flip = False

		if (label in dependency_dirs):
			if (not same_dep_order(dependency_dirs, src_dep_order, label)):
				orig_score += dependency_dirs[label][direction]
				rev_score += dependency_dirs[label][rev_direction]
			elif dependency_dirs[label][direction]<dependency_dirs[label][rev_direction]:
				skipped += 1
		if rev_score>orig_score:
			before = not before
			changed += 1
			flip = True
			
		if before:
			before_head.append(dep)
		else:
			after_head.append(dep)
			#if not flip:
			#else:
			#	after_head.insert(0, dep)

	for dep in before_head:
		current_order += reorder(tree, dep, dependency_dirs, src_dep_order)
	if head>0:
		current_order += [head]

	for dep in after_head:
		current_order += reorder(tree, dep, dependency_dirs, src_dep_order)

	return current_order

gold_treebank_folder = os.path.abspath(sys.argv[1])+'/'

print 'reading dominant dependency orders from gold data'
gold_dependency_dirs = dict()
for lang in os.listdir(gold_treebank_folder):
	print lang
	gold_treebank = DependencyTree.load_trees_from_conll_file(gold_treebank_folder+lang)
	gold_dependency_dirs[lang] = dict()

	for tree in gold_treebank:
		for i, h in enumerate(tree.heads):
			label = tree.labels[i]
			if label in ignore_deps:
				continue
			head_pos = tree.tags[h-1] if h>0 else 'ROOT' 
			dep_pos = tree.tags[i]
			pos_match =  dep_pos + '-'+ head_pos

			if not label in gold_dependency_dirs[lang]:
				gold_dependency_dirs[lang][label] = [0, 0]
			direction = 1 if h>i+1 else 0
			gold_dependency_dirs[lang][label][direction] += 1

	for label in gold_dependency_dirs[lang].keys():
		all_ = gold_dependency_dirs[lang][label][0] + gold_dependency_dirs[lang][label][1]
		gold_dependency_dirs[lang][label][0] = float(gold_dependency_dirs[lang][label][0])/all_
		gold_dependency_dirs[lang][label][1] = float(gold_dependency_dirs[lang][label][1])/all_
		if gold_dependency_dirs[lang][label][0] > 0.75:
			gold_dependency_dirs[lang][label][0] = 1
			gold_dependency_dirs[lang][label][1] = -1
		elif gold_dependency_dirs[lang][label][1] > 0.75:
			gold_dependency_dirs[lang][label][0] = -1
			gold_dependency_dirs[lang][label][1] = 1
		else:
			gold_dependency_dirs[lang][label][1] = 0
			gold_dependency_dirs[lang][label][0] = 0


gold_treebank_folder = os.path.abspath(sys.argv[2])+'/'
print 'reading dominant dependency orders from projections'
dependency_dirs = dict()
for lang in os.listdir(gold_treebank_folder):
	print lang
	gold_treebank = DependencyTree.load_trees_from_conll_file(gold_treebank_folder+lang)
	dependency_dirs[lang] = dict()

	for tree in gold_treebank:
		for i, h in enumerate(tree.heads):
			label = tree.labels[i]
			if label in ignore_deps:
				continue
			head_pos = tree.tags[h-1] if h>0 else 'ROOT' 
			dep_pos = tree.tags[i]
			pos_match =  dep_pos + '-'+ head_pos

			if not label in dependency_dirs[lang]:
				dependency_dirs[lang][label] = [0, 0]
			direction = 1 if h>i+1 else 0
			dependency_dirs[lang][label][direction] += 1

	for label in dependency_dirs[lang].keys():
		all_ = dependency_dirs[lang][label][0] + dependency_dirs[lang][label][1]
		dependency_dirs[lang][label][0] = float(dependency_dirs[lang][label][0])/all_
		dependency_dirs[lang][label][1] = float(dependency_dirs[lang][label][1])/all_
		if dependency_dirs[lang][label][0] > 0.75:
			dependency_dirs[lang][label][0] = 1
			dependency_dirs[lang][label][1] = -1
		elif dependency_dirs[lang][label][1] > 0.75:
			dependency_dirs[lang][label][0] = -1
			dependency_dirs[lang][label][1] = 1
		else:
			dependency_dirs[lang][label][1] = 0
			dependency_dirs[lang][label][0] = 0

print 'reordering trees'
original_tree_folder = os.path.abspath(sys.argv[3])+'/'
output_folder = os.path.abspath(sys.argv[4])+'/'
for lang in os.listdir(original_tree_folder):
	print lang
	skipped, changed = 0,0
	orig_trees = DependencyTree.load_trees_from_conll_file(original_tree_folder+lang)
	final_writer = codecs.open(output_folder+lang, 'w')
	orig_score, reorder_score = 0, 0

	better, worst = 0, 0
	same_str, diff_str = 0, 0
	for i in range(len(orig_trees)):
		orig_score += score_tree(orig_trees[i], dependency_dirs[lang])

		order = reorder(orig_trees[i], 0, dependency_dirs[lang], gold_dependency_dirs[orig_trees[i].lang_id])
		new_tree = orig_trees[i].reorder_with_order(order)
		reorder_score += score_tree(new_tree, dependency_dirs[lang])
		final_writer.write(new_tree.conll_str()+'\n\n')

	print 'orig_score:', orig_score,  'reorder_score:', reorder_score, 'skipped', skipped, 'changed', changed
	final_writer.close()
