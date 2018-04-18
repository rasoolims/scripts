import os,sys,codecs,random,operator,math
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict
language_families = {'cop':'Afro-Asiatic' , 'ar':'Afro-Asiatic' , 'he':'Afro-Asiatic' , 'id':'Austroasiatic+austeronesian' , 'vi':'Austroasiatic+austeronesian' , 'lt':'Balto-Slavic' , 'lv':'Balto-Slavic' , 'eu':'Basque' , 'ja':'East asian' , 'ko':'East asian' , 'zh':'East asian' , 'et':'Finnic+Uralic+Turkic' , 'fi':'Finnic+Uralic+Turkic' , 'tr':'Finnic+Uralic+Turkic' , 'hu':'Finnic+Uralic+Turkic' , 'da':'Germanic' , 'de':'Germanic' , 'en':'Germanic' , 'nl':'Germanic' , 'no':'Germanic' , 'sv':'Germanic' , 'hi':'Indo-Iranian' , 'fa':'Indo-Iranian' , 'el':'Romance' , 'la':'Romance' , 'es':'Romance' , 'fr':'Romance' , 'it':'Romance' , 'pt':'Romance' , 'ro':'Romance' , 'bg':'Balto-Slavic' , 'cs':'Balto-Slavic' , 'hr':'Balto-Slavic' , 'pl':'Balto-Slavic' , 'ru':'Balto-Slavic' , 'sk':'Balto-Slavic' , 'sl':'Balto-Slavic' , 'uk':'Balto-Slavic'}
ignore_deps = set(['conj','cc','fixed','flat','compound','list','parataxis','orphan','goeswith','reparandum','punct','root','discourse','dep', '_','case','clf','det','mark'])

def score_tree(tree, dependency_dirs, pos_directions):
	a, a_ = 0, 0
	for i, h in enumerate(tree.heads):
		label = tree.labels[i]
		# head_pos = tree.tags[h-1] if h>0 else 'ROOT' 
		# dep_pos = tree.tags[i]
		# pos_match =  dep_pos + '-'+ head_pos

		direction = 1 if h>i+1 else 0
		if label in dependency_dirs:
			a += dependency_dirs[label][direction]
			a_ += 1
		# if pos_match in pos_directions:
		# 	a += pos_directions[pos_match][direction]
		# 	a_ += 1
	return a


def reorder(tree, head, dependency_dirs, pos_directions):
	a = 0
	before_head = list()
	after_head = list()
	current_order = []
	for dep in sorted(tree.reverse_tree[head]):
		label = tree.labels[dep-1]
		# head_pos = tree.tags[head-1] if head>0 else 'ROOT' 
		# dep_pos = tree.tags[dep - 1]
		# pos_match =  dep_pos + '-'+ head_pos

		direction = 1 if head>dep else 0
		rev_direction = 1 if head<dep else 0

		orig_score, rev_score = 0, 0
		before = True if head>dep else 0

		if dep_pos != 'PUNCT':
			if label in dependency_dirs:
				orig_score += dependency_dirs[label][direction]
				rev_score += dependency_dirs[label][rev_direction]
			# if pos_match in pos_directions:
			# 	orig_score +=pos_directions[pos_match][direction]
			# 	rev_score +=pos_directions[pos_match][rev_direction]
			if rev_score>orig_score:
				# print head,'->', dep
				a+= rev_score-orig_score
				before = not before
			
		if before:
			before_head.append(dep)
		else:
			after_head.append(dep)

	for dep in before_head:
		current_order += reorder(tree, dep, dependency_dirs, pos_directions)
	if head>0:
		current_order += [head]

	for dep in after_head:
		current_order += reorder(tree, dep, dependency_dirs, pos_directions)

	# for dep in tree.reverse_tree[head]:
	# 	a+= reorder(tree, dep, dependency_dirs, pos_directions)
	# print current_order
	return current_order


gold_treebank = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
orig_trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[2]))

dependency_dirs,pos_directions = dict(), dict()
for tree in gold_treebank:
	for i, h in enumerate(tree.heads):
		label = tree.labels[i]
		if label in ignore_deps:
			continue
		head_pos = tree.tags[h-1] if h>0 else 'ROOT' 
		dep_pos = tree.tags[i]
		pos_match =  dep_pos + '-'+ head_pos

		if not label in dependency_dirs:
			dependency_dirs[label] = [0, 0]
		direction = 1 if h>i+1 else 0
		dependency_dirs[label][direction] += 1

		# if not pos_match in pos_directions:
		# 	pos_directions[pos_match] = [0, 0]
		# pos_directions[pos_match][direction] += 1

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


# for label in pos_directions.keys():
# 	all_ = pos_directions[label][0] + pos_directions[label][1]
# 	pos_directions[label][0] = float(pos_directions[label][0])/all_
# 	pos_directions[label][1] = float(pos_directions[label][1])/all_
# 	if pos_directions[label][0] > 0.75:
# 		pos_directions[label][0] = 1
# 		pos_directions[label][1] = -1
# 	elif pos_directions[label][1] > 0.75:
# 		pos_directions[label][0] = -1
# 		pos_directions[label][1] = 1
# 	else:
# 		pos_directions[label][1] = 0
# 		pos_directions[label][0] = 0



final_writer = codecs.open(os.path.abspath(sys.argv[3]), 'w')
target_lang_id = sys.argv[4]
target_lang_family = language_families[target_lang_id]
orig_score, reorder_score = 0, 0

better, worst = 0, 0
same_str, diff_str = 0, 0
skipped = set()
for i in range(len(orig_trees)):
	orig_score += score_tree(orig_trees[i], dependency_dirs, pos_directions)
	source_language_family = language_families[orig_trees[i].lang_id]

	#if source_language_family != target_lang_family: 
	order = reorder(orig_trees[i], 0, dependency_dirs, pos_directions)
	new_tree = orig_trees[i].reorder_with_order(order)
	reorder_score += score_tree(new_tree, dependency_dirs, pos_directions)
	final_writer.write(new_tree.conll_str()+'\n\n')
	#else:
	#	skipped.add(orig_trees[i].lang_id)
	#	final_writer.write(orig_trees[i].conll_str()+'\n\n')

print 'orig_score:', orig_score,  'reorder_score:', reorder_score
final_writer.close()
print 'skipped', skipped