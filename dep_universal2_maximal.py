import os,sys,codecs, operator
from collections import defaultdict
from mst_dep_tree_loader import DependencyTree

separating_deps = {'nsubj','obj','iobj','csubj','ccomp','xcomp',
					'advcl','list','dislocated','parataxis','orphan','reparandum', 'vocative', 
					'discourse', 'expl','cop','root','dep','ROOT'}
non_separating_deps = {'nummod','acl','amod','det','case','mark','compound','fixed','flat',
						'goeswith','appos','aux','advmod','clf','nmod'}
# this is just for reminding myself.
conditioning_deps = {'punct','conj','cc','obl'}

relations = separating_deps | non_separating_deps | conditioning_deps

def is_separable(tree, head, dep, separation_sets):
	if head == 0: return True
	relation = tree.labels[dep-1]

	if not relation in relations:
		print relation
		if not relation in relations: print relation
		assert relation in relations
	dep_pos = tree.tags[dep-1]
	head_pos = tree.tags[head-1]

	if relation in separating_deps:
		return True

	if relation == 'conj':
		if head_pos=='VERB':
			return True
		else:
			return False

	if relation=='obl':
		if (head_pos == 'NOUN' or head_pos == 'PROPN'):
			return False
		else:
			return True

	return False


def assign_separations(tree, head, separation_sets, nonprojective_arcs):
	left_deps = sorted([d for d in tree.reverse_tree[head] if d<head], reverse = True)
	right_deps = sorted([d for d in tree.reverse_tree[head] if d>head])

	separate = False
	for dep in left_deps:
		if separate: separation_sets[head].add(dep)
		assign_separations(tree, dep, separation_sets, nonprojective_arcs)
		if not separate:
			if dep in nonprojective_arcs:
				separation_sets[head].add(dep)

			if len(separation_sets[dep])>0 or is_separable(tree, head, dep, separation_sets):
				separate = True
				separation_sets[head].add(dep)

	separate = False
	for dep in right_deps:
		if separate: separation_sets[head].add(dep)
		assign_separations(tree, dep, separation_sets, nonprojective_arcs)
		if not separate:
			if dep in nonprojective_arcs:
				separation_sets[head].add(dep)

			if len(separation_sets[dep])>0 or is_separable(tree, head, dep, separation_sets):
				separate = True
				separation_sets[head].add(dep)

	#print head,separation_sets[head]
		

def postprocess(tree, head, separation_sets):
	# taking care of obl for the case of verb being in the noun phrase
	if not head in separation_sets[tree.heads[head-1]] and tree.heads[head-1]!=0 and (tree.tags[tree.heads[head-1]-1]=='NOUN' or tree.tags[tree.heads[head-1]-1]=='PROPN'):
		#print dep,head, tree.heads[head-1],'obl'
		#print separation_sets[tree.heads[head-1]]
		return False
	deps = tree.reverse_tree[head]
	left_deps = {d for d in deps if d < head}
	right_deps = {d for d in deps if d > head}

	for d in deps:
		postprocess(tree, d, separation_sets)
		if d in separation_sets[head]:
			continue

		if d<head:
			for l in left_deps:
				if l>d and l in separation_sets[head]:
					separation_sets[head].add(d)
					break

		else:
			for r in right_deps:
				if r<d and r in separation_sets[head]:
					separation_sets[head].add(d)
					break

	joined = sorted(deps - separation_sets[head])

	if len(joined)>0:
		if joined[0]<head and (tree.labels[joined[0]-1]=='punct' or tree.labels[joined[0]-1]=='cc'):
			separation_sets[head].add(joined[0])
		if joined[-1]>head and (tree.labels[joined[-1]-1]=='punct' or tree.labels[joined[-1]-1]=='cc'):
			separation_sets[head].add(joined[-1])

def complete_with_deps(tree, i, span):
	deps = tree.reverse_tree[i]
	for d in deps:
		span.add(d)
		complete_with_deps(tree,d,span)

def obtain_non_recursive(tree, i, phrases, separation_sets):
	deps = tree.reverse_tree[i]

	span = deps - separation_sets[i]

	new_span = set()
	for s in span:
		new_span.add(s)
		complete_with_deps(tree, s, new_span)

	span = sorted(new_span | {i})

	if i!=0: phrases.append([span[0],span[-1],tree.tags[i-1]])

	for d in separation_sets[i]:
		obtain_non_recursive(tree, d, phrases, separation_sets)

def create_shallow_tree(tree, put_to_tag):
	phrases = []
	separation_sets = defaultdict(set)
	nonprojective_arcs = DependencyTree.get_nonprojective_arcs(tree.heads)
	assign_separations(tree, 0, separation_sets, nonprojective_arcs)
	postprocess(tree, 0, separation_sets)
	obtain_non_recursive(tree, 0, phrases, separation_sets)
	starts = {s:i for i,[s,e,p] in enumerate(phrases)}
	
	for starts, index in sorted(starts.iteritems(), key=lambda (k,v): (v,k)):
		phrase = phrases[index]
		if phrase[2]=='PROPN' or phrase[2]=='DET' or phrase[2]=='PRON' or phrase[2] == 'NOUN':
			phrase[2] = 'N'
		if phrase[2]=='VERB' or phrase[2]=='AUX':
			phrase[2] = 'V'
		if phrase[2]=='PUNCT' or phrase[2]=='SCONJ':
			phrase[2] = 'O'
		if phrase[2]=='ADV':
			phrase[2] = 'AV'
		if phrase[2]=='ADJ':
			phrase[2] = 'AJ'

		pl = phrase[2]+'P' if phrase[2]!='O' else 'O'
		tree.ftags[phrase[0]-1] = 'B-'+pl if pl!='O' else 'O'
		if phrase[1]>phrase[0]:
			for i in range(phrase[0]+1,phrase[1]+1):
				tree.ftags[i-1] = 'I-'+pl if  pl!='O' else 'O'

	if not put_to_tag:
		return tree.chunk_str()+'\n\n'
	else:
		return tree.conll_str()+'\n\n'

print 'reading trees'
t = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')

put_to_tag = False if len(sys.argv)<4 or sys.argv[3]!='tag' else True

print 'writing trees'
full = 0
for tree in t:
	for i in xrange(len(tree.ftags)):
		tree.ftags[i] = '_'
	#print ' '.join(tree.words)
	writer.write(create_shallow_tree(tree, put_to_tag))
	is_full = True
	for i in xrange(len(tree.ftags)):
		if tree.ftags[i] == '_':
			is_full = False
			break
	if is_full:
		full+=1
writer.close()
print 'num of full',full,'out of',len(t)
