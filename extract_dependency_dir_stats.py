from mst_dep_tree_loader import DependencyTree
import os, sys, math, operator, codecs

#def_log = math.log(0.5)

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

target_trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
target_lang = sys.argv[2]
tree_dir = os.path.abspath(sys.argv[3])+'/'
max_num = int(sys.argv[4])
dic_folder = os.path.abspath(sys.argv[5])+'/'
output_path = os.path.abspath(sys.argv[6])

dependency_dirs = dict()
pos_directions = dict()

all_ = 0
for tree in target_trees:
	all_ += len(tree.labels)
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

print 'reading dictionaries...'
c = 0
dictionaries = dict()
for f in os.listdir(dic_folder):
	dictionaries[f]= dict()
	l1, l2 = f.split('2')
	if l2 != target_lang:
		continue

	rec = codecs.open(dic_folder+f,'r').read().strip().split('\n')
	for r in rec:
		spl = r.split('\t')
		dictionaries[f][spl[0]] = spl[1]
	# print f, len(dictionaries[f])
	c+=1
	if c%100==0:
		sys.stdout.write(str(c)+'...')
print '!'


source_trees = dict()

for f in os.listdir(tree_dir):
	if f == target_lang:
		continue
	

	s_t = DependencyTree.load_trees_from_conll_file(tree_dir+f)

	for t in s_t:
		if len(t.heads)<100:
			source_trees[t] = score_tree(t, dependency_dirs, pos_directions)
	print f, len(source_trees)

st = sorted(source_trees.items(), key=operator.itemgetter(1), reverse=True)
output_trees = []
c = 0


for t in st:
	tree = t[0]
	l_id = tree.lang_id
	dct = dictionaries[l_id+'2'+target_lang]
	#todo lexicalization as well!
	for i in range(len(tree.words)):
		tree.words[i] = tree.words[i].lower() 
		if tree.words[i] in dct:
			tree.lemmas[i] = tree.words[i] 
			tree.words[i] = dct[tree.words[i]]

	output_trees.append(tree.conll_str())
	c+= 1
	if c>= max_num:
		break
	if c<10:
		print t[1]

codecs.open(output_path, 'w').write('\n\n'.join(output_trees)+'\n')