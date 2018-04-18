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

gold_treebank = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
orig_trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[2]))
reorder_trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[3]))

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



assert len(orig_trees) == len(reorder_trees)
final_writer = codecs.open(os.path.abspath(sys.argv[4]), 'w')
orig_score, reorder_score, mix_score = 0, 0, 0

better, worst, same = 0, 0 , 0
same_str, diff_str = 0, 0
better_lang, worst_lang, same_lang = defaultdict(int),defaultdict(int),defaultdict(int)
langs = set()
for i in range(len(orig_trees)):
	score_orig = score_tree(orig_trees[i], dependency_dirs, pos_directions)
	score_reorder = score_tree(reorder_trees[i], dependency_dirs, pos_directions)
	orig_score += score_orig
	reorder_score += score_reorder
	mix_score += max(score_orig, score_reorder)
	if score_orig < score_reorder:
		better += 1
		better_lang[orig_trees[i].lang_id]+=1
	elif score_orig > score_reorder:
		worst += 1
		worst_lang[orig_trees[i].lang_id]+=1
	else:
		same += 1
		same_lang[orig_trees[i].lang_id]+=1
	langs.add(orig_trees[i].lang_id)

	orig_str = ' '.join([orig_trees[i].lemmas[j] for j in range(0,len(orig_trees[i].words))])
	reorder_str =' '.join([reorder_trees[i].lemmas[j] for j in range(0,len(reorder_trees[i].words))])
	final_writer.write(orig_str+'\n')
	if orig_str == reorder_str:
		same_str += 1
	else:
		diff_str += 1
		final_writer.write(reorder_str+'\n')
		final_writer.write(str(score_orig)+'->'+str(score_reorder)+'\n')
	final_writer.write('\n')
for lang_id in sorted(langs):
	print lang_id,  'worst:', worst_lang[lang_id], 'same:',same_lang[lang_id], 'better:', better_lang[lang_id] 

print 'worst:', worst, 'same:',same, 'better:', better 
print 'same_str:', same_str, 'diff_str:', diff_str
print 'orig_score:', orig_score,  'reorder_score:', reorder_score, 'mix_score:', mix_score
final_writer.close()