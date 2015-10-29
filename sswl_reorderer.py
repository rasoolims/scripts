import os,sys,codecs,random,operator,math
from collections import namedtuple
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
				#print 'sbj verb'
				assignemnts[i] = 'r'
			elif c>h and not 'verb sbj' in rules:
				#print 'verb sbj'
				assignemnts[i] = 'l'

		# object relation
		if 'obj' in l and ch =='VERB':
			if c<h and not 'obj verb' in rules:
				#print 'obj verb'
				assignemnts[i] = 'r'
			elif c>h and not 'verb obj' in rules:
				#print  'verb obj' 
				assignemnts[i] = 'l'

		# adposition noun
		if ch == 'ADP' and cp =='NOUN':
			if c>h and not 'adp noun' in rules:
				#print c,h,'adp noun'
				assignemnts[i] = 'r'
			elif c<h and not 'noun adp' in rules:
				#print c,h,'noun adp'
				assignemnts[i] = 'l'

		# adjective noun
		if cp == 'ADJ' and ch =='NOUN':
			if c<h and not 'adj noun' in rules:
				#print 'adj noun'
				assignemnts[i] = 'r'
			elif c>h and not 'noun adj' in rules:
				#print 'noun adj'
				assignemnts[i] = 'l'

		# numerical noun
		if cp == 'NUM' and ch =='NOUN':
			if c<h and not 'num noun' in rules:
				#print 'num noun' 
				assignemnts[i] = 'r'
			elif c>h and not 'noun num' in rules:
				#print  'noun num' 
				assignemnts[i] = 'l'

		if 'num' == l and ch =='VERB':
			if c<h and not 'num noun' in rules:
				#print  'num noun' 
				assignemnts[i] = 'r'
			elif c>h and not 'noun num' in rules:
				#print 'noun num' 
				assignemnts[i] = 'l'

		# demonstrative noun
		if 'det' == l and ch =='NOUN':
			if c<h and not 'det noun' in rules:
				#print 'det noun'
				assignemnts[i] = 'r'
			elif c>h and not 'noun det' in rules:
				#print 'noun det'
				assignemnts[i] = 'l'

		# possesive noun
		if 'poss' == l and ch =='NOUN':
			if c<h and not 'poss noun' in rules:
				#print 'poss noun'
				assignemnts[i] = 'r'
			elif c>h and not 'noun poss' in rules:
				#print 'noun poss'
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

def getright_words(tree, p,children, r, h):
	if r.has_key(h):
		return r[h]
	r[h]=set()
	for c in  tree.reverse_tree[h]:
		cr = getright_words(tree, p,children, r, c)
		if p[c-1]=='r':
			r[h].add(c)
			r[h] = r[h] | cr  | children[c]
	if  h>0 and p[h-1] == 'l':
		r[h].add(tree.heads[h-1])
		r[h] = r[h] | getright_words(tree, p,children, r, tree.heads[h-1])

	return r[h]

def getleft_words(tree, p, children, l, h):
	if l.has_key(h):
		return l[h]
	l[h]=set()
	l[h].add(0)
	if h==0:
		return l[h]
	for c in tree.reverse_tree[h]:
		cl = getleft_words(tree, p,children, l, c)
		if p[c-1]=='l':
			l[h].add(c)
			l[h] = l[h] | cl | children[c]
	if h>0 and p[h-1] == 'r':
		l[h].add(tree.heads[h-1])
		l[h] = l[h]  | getleft_words(tree, p,children, l, tree.heads[h-1])

	return l[h]

def complete_left_right_set(s):
	s2 = dict()
	for i in s.keys():
		s2[i] = s[i]
		for j in s[i]:
			s2[i] = s2[i] | s[j]
	return s2

def recursive_reorder_with_assignments(orig_tree, tree, p, h):
	if len(orig_tree.reverse_tree[h])==0:
		return tree
	#print '->',h
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
	#print h,ordering
	if h !=0:
		new_tree = new_tree.reorder(new_tree.reverse_index[h],ordering)
	else:
		#print ' '.join(new_tree.words)
		return new_tree
	#print ' '.join(new_tree.words)
	return new_tree 


def reorder_based_on_lm(tree, l, r, lm, beam, position, max_beam_size):
	new_beam = list()
	BeamElement = namedtuple("BeamElement", ["sequence","elements", "tag_dict","score"])

	for element in beam:
		sc = element.score
		#print element.sequence
		tags = list()
		for e in element.sequence:
			tags.append(tree.words[e-1])

		last_word_index = 0 if len(element.sequence)==0 else element.sequence[-1]

		for t in element.tag_dict:
			if position==1 and len(l[t])>1:
				#print '>',t
				continue
			if t in l[last_word_index]:
				#if position==1:
					#print '<>',t,last_word_index
				continue

			if last_word_index in r[t]:
				#if position==1:
					#print '><',t,last_word_index
				continue

			should_ignore = False
			for t_prime in element.tag_dict:
				if t!=t_prime and (t in r[t_prime] or t_prime in l[t]):
					should_ignore = True
					break

			if should_ignore:
				continue

			seq = list(element.sequence)
			seq.append(t)
			remain = set(element.tag_dict)
			remain.remove(t)
			new_element = list(element.elements)
			new_element.append(tree.tags[t-1])

			five_gram = new_element[-5:]
			prob = lm.score_gram(five_gram)

			score = sc + prob

			beam_element = BeamElement(sequence=seq, elements= new_element,tag_dict=remain,score=score)

			new_beam.append(beam_element)

	if position == len(tree.words):
		newer_beam = list()
		for beam_element in new_beam:
			elem = beam_element.elements
			elem.append('</s>')
			sc = beam_element.score + lm.score_gram(elem)

			new_beam_element = BeamElement(sequence=beam_element.sequence, elements= elem,tag_dict=beam_element.tag_dict, score = sc) 
			newer_beam.append(new_beam_element)
		new_beam = newer_beam

	if len(new_beam)==0:
		seq = list()
		for i in range(0,len(tree.words)):
			seq.append(i+1)
		for elem in beam:
			print elem.sequence
		print 'failed to find'
		return seq

	new_beam.sort(key=lambda x:x.score)
	if position == len(tree.words):
		return new_beam[0].sequence

	beam = list()
	ln = len(new_beam) -1
	for i in range(0, min(ln+1,max_beam_size)):
		beam.append(new_beam[ln-i])

	return reorder_based_on_lm(tree, l, r, lm, beam, position+1, max_beam_size)


rules = readrules(os.path.abspath(sys.argv[1]))
trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[2]))
lang_model = LanguageModel(os.path.abspath(sys.argv[3]))
writer = codecs.open(os.path.abspath(sys.argv[4]),'w')
writer2 = codecs.open(os.path.abspath(sys.argv[4])+'.reordered_lm','w')

BeamElement = namedtuple("BeamElement", ["sequence","elements", "tag_dict","score"])

for tree in trees:
	if not DependencyTree.is_projective(tree.heads):
		continue

	s1 =  ' '.join(tree.words)
	p = assign_positions(tree,rules)
	r = dict()
	l = dict()
	children = dict()
	get_children(tree,children,0)
	for i in range(0,len(tree.words)+1):
		getright_words(tree, p,children, r, i)
		getleft_words(tree, p,children, l, i)

	#l = complete_left_right_set(l)
	#r= complete_left_right_set(r)
	
	nt = tree
	new_tree = recursive_reorder_with_assignments(tree, nt, p, 0)
	s2 = ' '.join(new_tree.words)

	#if s1!=s2:
		#print tree.conll_str()
		#print '\t'.join(p)
		#print '\n'+s1+'\n'+s2+'\n\n'
	writer.write(new_tree.conll_str().strip()+'\n\n')

	beam = list()
	tag_dict = set()
	for i in range(1,len(tree.words)+1):
		tag_dict.add(i)
	first_element = BeamElement(sequence = list(),elements=list(), tag_dict = tag_dict, score = 0) 
	beam.append(first_element)
	
	l2 = dict()
	r2 = dict()
	for i in r.keys():
		rev_i = 0 if i ==0 else new_tree.reverse_index[i]
		l2[rev_i] = set()
		r2[rev_i] = set()

		for x in l[i]:
			rev_x =  0 if x ==0 else new_tree.reverse_index[x]
			l2[rev_i].add(rev_x)

		for x in r[i]:
			rev_x = 0 if x ==0 else  new_tree.reverse_index[x]
			r2[rev_i].add(rev_x)

	#print new_tree.words
	#print children
	#print l
	#print r
	#print '------------------------------------------------------'
	#print l2
	#print r2
	new_order = reorder_based_on_lm(new_tree, l2,r2, lang_model,beam,1,100)
	rev_order = list()
	for n in new_order:
		rev_order.append(n)

	new_words = list()
	new_tags = list()
	new_heads = list()
	new_labels = list()
	for n in new_order:
		new_words.append(new_tree.words[n-1])
		new_tags.append(new_tree.tags[n-1])
		new_labels.append(new_tree.labels[n-1])
		new_heads.append(rev_order[new_tree.heads[n-1]-1])

	reordered_tree = DependencyTree(new_words, new_tags, new_heads, new_labels)

	the_same = True
	for i in range(0,len(new_order)):
		if new_order[i]!=i+1:
			the_same = False
			break
	
	if not the_same:
		print new_tree.reverse_index
		print p
		#for i in range(0,len(tree.words)):
			#writer2.write(str(i)+'\n')
			#writer2.write(' '.join([str(x) for x in l[i]])+'\n')
			#writer2.write(' '.join([str(x) for x in r[i]])+'\n')
		ordd = ' '.join([str(x) for x in new_order])
		print l2
		print r2
		print ordd+'\n'
		print new_tree.conll_str()+'\n\n'
		print reordered_tree.conll_str()+'\n\n'
		if DependencyTree.is_projective(new_heads):
			print 'non-projective'
		#writer2.write(str(the_same)+'\t'+ordd+'-->\n')
	#writer2.write(new_tree.conll_str()+'\n\n')
	writer2.write(reordered_tree.conll_str()+'\n\n')


writer.close()	
writer2.close()

