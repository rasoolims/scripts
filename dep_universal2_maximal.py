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

def is_separable(tree, head, dep):
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
		if (head_pos == 'NOUN' or head_pos == 'PROPN' or head_pos=='DET' or head_pos=='NUM' or head_pos=='PRON'):
			return False
		else:
			return True

	return False


def belongs_to(tree, h, dep):
	belongs = True
	if h>dep:
		for i in range(dep+1, h):
			print h,dep,i,tree.labels[i-1]
			if i in tree.reverse_tree[h]:
				if (tree.labels[i-1] in separating_deps):
					belongs = False
					print '#1',(tree.labels[i-1] in separating_deps)
					break
			elif not (tree.heads[i-1]>=dep and tree.heads[i-1]<h):
				belongs = False
				print '#2'
				break
			elif tree.labels[i-1] in separating_deps:
				belongs = False
				print '#3'
				break
	else:
		for i in range(h+1, dep):
			if i in tree.reverse_tree[h]:
				if (tree.labels[i-1] in separating_deps):
					belongs = False
					print '#1'
					break
			elif not (tree.heads[i-1]<=dep and tree.heads[i-1]>h):
				belongs = False
				print '#2'
				break
			elif tree.labels[i-1] in separating_deps:
				belongs = False
				print '#3'
				break
	print 'belongs',h,dep,belongs
	return belongs

def assign_separations(tree, head, separation_sets, nonprojective_arcs):
	left_deps = sorted([d for d in tree.reverse_tree[head] if d<head], reverse = True)
	right_deps = sorted([d for d in tree.reverse_tree[head] if d>head])

	separate = False
	for dep in left_deps:
		if separate: separation_sets[head].add(dep)
		assign_separations(tree, dep, separation_sets, nonprojective_arcs)
		if  (dep in nonprojective_arcs) and not belongs_to(tree, head, dep):
				separation_sets[head].add(dep)
				separate = True
		if not separate:
			if is_separable(tree, head, dep):
				separate = True
				separation_sets[head].add(dep)
			if len(separation_sets[dep])>0:
				for d in separation_sets[dep]:
					if is_separable(tree, dep, d):
						separate = True
						separation_sets[head].add(dep)
						break

	separate = False
	for dep in right_deps:
		if separate: separation_sets[head].add(dep)
		assign_separations(tree, dep, separation_sets, nonprojective_arcs)
		if (dep in nonprojective_arcs) and not belongs_to(tree, head, dep):
			separation_sets[head].add(dep)
			separate = True
		if not separate:
			if is_separable(tree, head, dep):
				separate = True
				separation_sets[head].add(dep)
			if len(separation_sets[dep])>0:
				for d in separation_sets[dep]:
					if is_separable(tree, dep, d):
						separate = True
						separation_sets[head].add(dep)
						break

	#print head,separation_sets[head]


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

	while len(joined)>0:
		print 'joined',head,joined
	 	if joined[0]<head and (tree.labels[joined[0]-1]=='punct' or tree.labels[joined[0]-1]=='cc'):
	 		separation_sets[head].add(joined[0])
	 		del joined[0]
	 	elif joined[-1]>head and (tree.labels[joined[-1]-1]=='punct' or tree.labels[joined[-1]-1]=='cc'):
	 		separation_sets[head].add(joined[-1])
	 		del joined[-1]
	 	else: break
def complete_with_deps(tree, i, span, separation_sets):
	deps = tree.reverse_tree[i]
	for d in deps:
		#if not d in separation_sets[i]:
			span.add(d)
			complete_with_deps(tree,d,span, separation_sets)
		#else: print 'not added',i,d

def obtain_non_recursive(tree, i, phrases, separation_sets):
	deps = tree.reverse_tree[i]

	span = deps - separation_sets[i]
	#print '->',i,span

	new_span = set()
	for s in span:
		new_span.add(s)
		complete_with_deps(tree, s, new_span, separation_sets)

	span = sorted(new_span | {i})

	if i!=0: 
		#print [span[0],span[-1],tree.tags[i-1]]
		phrases.append([span[0],span[-1],tree.tags[i-1]])

	for d in separation_sets[i]:
		obtain_non_recursive(tree, d, phrases, separation_sets)


def create_shallow_tree(tree, put_to_tag):
	phrases = []
	separation_sets = defaultdict(set)
	nonprojective_arcs = DependencyTree.get_nonprojective_arcs(tree.heads)
	assign_separations(tree, 0, separation_sets, nonprojective_arcs)
	print 'nonprojective_arcs',nonprojective_arcs
	postprocess(tree, 0, separation_sets)
	
	obtain_non_recursive(tree, 0, phrases, separation_sets)
	starts = {s:i for i,[s,e,p] in enumerate(phrases)}
	
	for starts, index in sorted(starts.iteritems(), key=lambda (k,v): (v,k)):
		phrase = phrases[index]
		if phrase[2] in {'NUM' , 'PROPN' , 'DET' , 'PRON' , 'NOUN'}:
			if phrase[0]==phrase[1] and phrase[2]=='DET':
				phrase[2] = 'O'
			else:
				phrase[2] = 'N'
		if phrase[2]=='VERB' or phrase[2]=='AUX':
			phrase[2] = 'V'
		if phrase[2] in {'PUNCT' , 'SCONJ' , 'CCONJ' , 'INTJ' , 'PART' , 'SYM' , 'X', 'ADP'}:
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
	print ' '.join(tree.words)
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
