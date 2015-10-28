import os,sys,codecs,random,operator,math
from mst_dep_tree_loader import DependencyTree
from languagemodel import LanguageModel
from reorderer import Reorderer

def readrules(input_path):
	return set(open(input_path,'r').read().strip().split('\n'))

def assign_positions(tree, rules):
	assignemnts = ['']*len(tree.heads)

	for i in range(0,len(tree.heads)):
		c = i+1
		h = tree.heads[i]

		if c<h:
			assignemnts[i] = 'l'
		else:
			assignemnts[i] = 'r'

		l = tree.labels[i]
		cp = tree.tags[i]
		ch = 'ROOT' if h==0 else tree.tags[h-1]

		# subject relation
		if 'subj' in l and ch =='VERB':
			if c<h and not 'sbj verb' in rules:
				print 'sbj verb'
				assignemnts[i] = 'r'
			elif c>h and not 'verb sbj' in rules:
				print 'verb sbj'
				assignemnts[i] = 'l'

		# object relation
		if 'obj' in l and ch =='VERB':
			if c<h and not 'obj verb' in rules:
				print 'obj verb'
				assignemnts[i] = 'r'
			elif c>h and not 'verb obj' in rules:
				print  'verb obj' 
				assignemnts[i] = 'l'

		# adposition noun
		if cp == 'ADP' and ch =='NOUN':
			if c<h and not 'adp noun' in rules:
				print 'adp noun'
				assignemnts[i] = 'r'
			elif c>h and not 'noun adp' in rules:
				print 'noun adp'
				assignemnts[i] = 'l'

		# adjective noun
		if cp == 'ADJ' and ch =='NOUN':
			if c<h and not 'adj noun' in rules:
				print 'adj noun'
				assignemnts[i] = 'r'
			elif c>h and not 'noun adj' in rules:
				print 'noun adj'
				assignemnts[i] = 'l'

		# numerical noun
		if cp == 'NUM' and ch =='NOUN':
			if c<h and not 'num noun' in rules:
				print 'num noun' 
				assignemnts[i] = 'r'
			elif c>h and not 'noun num' in rules:
				print  'noun num' 
				assignemnts[i] = 'l'

		if 'num' == l and ch =='VERB':
			if c<h and not 'num noun' in rules:
				print  'num noun' 
				assignemnts[i] = 'r'
			elif c>h and not 'noun num' in rules:
				print 'noun num' 
				assignemnts[i] = 'l'

		# demonstrative noun
		if 'det' == l and ch =='NOUN':
			if c<h and not 'det noun' in rules:
				print 'det noun'
				assignemnts[i] = 'r'
			elif c>h and not 'noun det' in rules:
				print 'noun det'
				assignemnts[i] = 'l'

		# possesive noun
		if 'poss' == l and ch =='NOUN':
			if c<h and not 'poss noun' in rules:
				print 'poss noun'
				assignemnts[i] = 'r'
			elif c>h and not 'noun poss' in rules:
				print 'noun poss'
				assignemnts[i] = 'l'

	return assignemnts

def get_children(tree, c, head):
	if c.has_key(head):
		return c[head]

	else:
		c[head] = set()
		for ch in tree.reverse_tree[head]:
			c[head].add(ch)
			c[head] = c[head] | get_children(tree, c, ch)
		return c[head]

def getright_words(tree, p, r, h):
	if r.has_key(h):
		return r[h]
	r[h]=set()
	for c in tree.reverse_tree[h]:
		cr = getright_words(tree, p, r, c)
		if p[c-1]=='r':
			r[h].add(c)
			r[h] = r[h] | cr
	if  h>0 and p[h-1] == 'l':
		r[h].add(tree.heads[h-1])
		r[h] = r[h] | r[tree.heads[h-1]]

	return r[h]

def getleft_words(tree, p, l, h):
	if l.has_key(h):
		return l[h]
	l[h]=set()
	for c in tree.reverse_tree[h]:
		cl = getleft_words(tree, p, l, c)
		if p[c-1]=='l':
			l[h].add(c)
			l[h] = l[h] | cl
	if h>0 and p[h-1] == 'r':
		l[h].add(tree.heads[h-1])
		l[h] = l[h] | l[tree.heads[h-1]]

	return l[h]

def recursive_reorder_with_assignments(orig_tree, tree, p, h):
	if len(orig_tree.reverse_tree[h])==0:
		return tree

	left = list()
	middle = list()
	right = list()
	i = 0

	c_h = list()
	c_h.append(h)
	for c in sorted(orig_tree.reverse_tree[h]):
		c_h.append(c) 

	new_tree = tree
	for c in sorted(c_h):
		if c == h:
			middle.append(i)
			i += 1
			continue

		if p[c-1] =='l':
			new_tree = recursive_reorder_with_assignments(orig_tree, new_tree, p, c)
			left.append(i)
		else:
			new_tree = recursive_reorder_with_assignments(orig_tree, new_tree, p, c)
			right.append(i)
		i+=1

	ordering = left + middle + right
	if h !=0:
		new_tree = new_tree.reorder(new_tree.reverse_index[h],ordering)
	else:
		return new_tree
	return new_tree 

rules = readrules(os.path.abspath(sys.argv[1]))
trees = DependencyTree.load_trees_from_file(os.path.abspath(sys.argv[2]))

for tree in trees:
	s1 =  ' '.join(tree.words)
	p = assign_positions(tree,rules)
	r = dict()
	l = dict()
	getright_words(tree, p, r, 0)
	getleft_words(tree, p, l, 0)
	c = dict()
	get_children(tree,c,0)
	
	

	nt = tree
	new_tree = recursive_reorder_with_assignments(tree, nt, p, 0)
	s2 = ' '.join(new_tree.words)

	if s1!=s2:
		print tree.tree_str()
		print '\t'.join(p)
		print '\n'+s1+'\n'+s2+'\n\n'
	

