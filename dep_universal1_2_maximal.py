import os,sys,codecs, operator
from collections import defaultdict
from mst_dep_tree_loader import DependencyTree

separating_deps = {'nsubj','nsubjpass','dobj','iobj','csubj','csubjpass','ccomp','xcomp','acl',
					'advcl','list','dislocated','parataxis','remnant','reparandum', 'vocative', 
					'discourse', 'expl','cop','mark','root','dep','appos','ROOT'}
non_separating_deps = {'nummod','amod','det','neg','case','advmod','compound','name','mwe',
						'foreign','goeswith','aux','auxpass'}
# this is just for reminding myself.
conditioning_deps = {'nmod','punct','conj','cc'}

relations = separating_deps | non_separating_deps | conditioning_deps

def is_separable(tree, head, dep):
	if head == 0: return True
	relation = tree.labels[dep-1]

	if not relation in relations:
		print relation
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

	if relation == 'nmod':
		if head_pos == 'NOUN':
			return False
		else:
			return True

	return False


def assign_separations(tree, head, separation_sets, nonprojective_arcs):
	deps = tree.reverse_tree[head]

	for dep in deps:
		assign_separations(tree, dep, separation_sets, nonprojective_arcs)
		if dep in nonprojective_arcs:
			separation_sets[head].add(dep)
		if len(separation_sets[dep])>0 or is_separable(tree, head, dep):
			separation_sets[head].add(dep)

def postprocess(tree, head, separation_sets):
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

def create_shallow_tree(tree):
	phrases = []
	separation_sets = defaultdict(set)
	nonprojective_arcs = DependencyTree.get_nonprojective_arcs(tree.heads)
	assign_separations(tree, 0, separation_sets, nonprojective_arcs)
	postprocess(tree, 0, separation_sets)
	obtain_non_recursive(tree, 0, phrases, separation_sets)
	starts = {s:i for i,[s,e,p] in enumerate(phrases)}
	
	for starts, index in sorted(starts.iteritems(), key=lambda (k,v): (v,k)):
		phrase = phrases[index]
		pl = phrase[2]+'P'
		tree.ftags[phrase[0]-1] = 'B-'+pl
		if phrase[1]>phrase[0]:
			for i in range(phrase[0]+1,phrase[1]+1):
				tree.ftags[i-1] = 'I-'+pl

	return tree.chunk_str()+'\n\n'

print 'reading trees'
t = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')

print 'writing trees'
dropped = 0
for tree in t:
	writer.write(create_shallow_tree(tree))
writer.close()
