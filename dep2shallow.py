import os,sys,codecs, operator
from mst_dep_tree_loader import DependencyTree

def tag2phrase(tag):
	return tag+'P'

def tag2unique_phrase(word, tag):
	return word +'\t'+tag+'\tB-'+tag2phrase(tag)

def obtain_non_recursive(tree, i, cur):
	deps = tree.reverse_tree[i]
	is_recursive = False
	for d in deps:
		obtain_non_recursive(tree, d, cur)
		if len(tree.reverse_tree[d])>0:
			is_recursive = True

	if not is_recursive:
		cur.append(i)

def create_shallow_tree(tree):
	cur = list()
	obtain_non_recursive(tree, 0, cur)
	cur = sorted(cur)

	output = dict()
	
	for c in cur:
		phrase = tag2phrase(tree.tags[c-1])
		members = sorted(list(tree.reverse_tree[c]) + [c])
		output[members[0]] = tree.words[members[0]-1] +' '+tree.tags[members[0]-1]+ ' B-'+phrase
		for i in range(1, len(members)):
			output[members[i]] = tree.words[members[i]-1] +' '+tree.tags[members[i]-1]+ ' I-'+phrase

	final_res = list()
	for i in range(1, len(tree.words)+1):
		if not output.has_key(i):
			output[i] = tree.words[i-1] +' '+tree.tags[i-1]+ ' B-'+tag2phrase(tree.tags[i-1])
		final_res.append(output[i])
	return '\n'.join(final_res)+'\n\n'

print 'reading trees'
t = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')

print 'writing trees'
dropped = 0
for tree in t:
	if DependencyTree.is_projective(tree.heads):
		writer.write(create_shallow_tree(tree))
	else:
		dropped+=1
writer.close()
print 'dropped', dropped