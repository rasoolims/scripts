import os,sys,codecs
from mst_dep_tree_loader import DependencyTree

def tag2phrase(tag):
	if tag == 'ADJ':
		return 'AJP'
	elif tag == 'ADP':
		return 'PP'
	elif tag == 'ADV':
		return 'ADVP'
	elif tag == 'CONJ':
		return 'CONJP'
	elif tag == 'DET':
		return 'DP'
	elif tag == 'NOUN':
		return 'NP'
	elif tag == 'PRON':
		return 'PRNP'
	elif tag == 'NUM':
		return 'NUMP'
	elif tag == 'PRT':
		return 'PRTP'
	elif tag == 'VERB':
		return 'VP'
	elif tag == 'X':
		return 'XP'
	elif tag == '.':
		return 'PUNCP'
	else:
		return tag+'P'

def recursive_phrase(tree, i):
	tag = tree.tags[i-1]
	word = tree.words[i-1]

	if tree.reverse_tree.has_key(i):
		deps = tree.reverse_tree[i]
		prev = list()
		nxt = list()
		for d in deps:
			p = recursive_phrase(tree,d)
			prev.append(p) if d<i else nxt.append(p)
		phrse = tag2phrase(tag)
		return '[_'+phrse+' '+' '.join(prev)+' '+word+'_'+tag+' '+' '.join(nxt)+' ]_'+phrse
	else:
		return word+'_'+tag


print 'reading trees'
t = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')

print 'writing trees'
for tree in t:
	if DependencyTree.is_projective(tree.heads):
		output = list()
		for dep in tree.reverse_tree[0]:
			output.append(' [_S '+recursive_phrase(tree,dep)+' ]_S')
		writer.write('[ '+' '.join(output)+' ]\n\n')
writer.close()