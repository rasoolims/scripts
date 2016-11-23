import os,sys,codecs,operator,itertools,math,gc
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict

def tag2phrase(tag):
	return tag+'P'

def tag2unique_phrase(word, tag):
	return word +'\t'+tag+'\tB-'+tag2phrase(tag)

def extract_ngram_probs(tree_path):
	print 'reading target trees'
	t = DependencyTree.load_trees_from_conll_file(tree_path)

	print 'estimating probabilities'
	bigram_count = defaultdict(int)
	trigram_count = defaultdict(float)
	for tree in t:
		tags = ['<s>','<s>'] +tree.tags +['</s>']

		for i in range(0, len(tags)-2):
			bigram = tags[i]+' '+tags[i+1]
			trigram = bigram+' '+tags[i+2]

			bigram_count[bigram]+=1
			trigram_count[trigram]+=1.0

	for trigram in trigram_count.keys():
		bigram = trigram.split(' ')[0]+' '+trigram.split(' ')[1]
		trigram_count[trigram]=trigram_count[trigram]/bigram_count[bigram]

	return trigram_count

def obtain_non_recursive(tree, i, cur, non_cur):
	deps = tree.reverse_tree[i]
	is_recursive = False
	for d in deps:
		if len(tree.reverse_tree[d])>0:
			is_recursive = True
			break

	if not is_recursive:
		cur.append(i)
	else:
		if i!=0:
			non_cur.append(i)
		for d in deps:
			obtain_non_recursive(tree, d, cur, non_cur)

def reorder_next_span(ngram_probs, current_beam, k, tree, spans, index):
	permutations = list(itertools.permutations(spans[index])) if len(spans[index])>1 and len(spans[index])<6 else [spans[index]]
	eps = math.log(1e-20)
	new_beam = dict()
	items = dict()
	ind = 0
	orig_gram = [tree.tags[i-1] for i in spans[index]]
	for b in current_beam:
		for p in permutations:
			ngrams = b[0][-2:] + [tree.tags[i-1] for i in p]
			if index == len(spans)-1:
				ngrams+= ['</s>']
			score = b[1]
			for i in xrange(len(ngrams)-2):
				prob = ngram_probs[' '.join(ngrams[i:i+3])]
				score += math.log(prob) if prob>0 else eps

			beam_element = b[2] + list(p)
			cur_gram = [tree.tags[i-1] for i in p]

			if cur_gram!=orig_gram:
				beam_element = b[2] + list(p)
			else:
				beam_element = b[2] + spans[index]

			items[ind]=(cur_gram, score, beam_element)
			new_beam[ind] = score

	sorted_beam = sorted(new_beam.items(), key=operator.itemgetter(1), reverse = True)
	final_beam = []
	
	[final_beam.append(items[sorted_beam[i][0]]) for i in xrange(min(k,len(sorted_beam)))]

	if index<len(spans)-1:
		return reorder_next_span(ngram_probs,final_beam, k, tree, spans, index+1)
	else:
		return final_beam[0]

def reoder_tree(ngram_probs, tree, beam_size):
	cur = []
	non_cur = []
	obtain_non_recursive(tree, 0, cur, non_cur)
	all_spans = sorted(cur+non_cur)
	spans = []

	for c in all_spans:
		if c in cur:
			members = sorted(filter(None,list(tree.reverse_tree[c]) + [c]))
			spans.append(members)
		else:
			spans.append([c])

	init_beam = [(['<s>','<s>'],0,list())]
	final_order = reorder_next_span(ngram_probs,init_beam, beam_size, tree, spans, 0)
	new_order = []
	rev_order = dict()
	[new_order.append(i) for i in final_order[2]]
	for i in xrange(len(new_order)):
		rev_order[new_order[i]]=i+1
	new_words = []
	[new_words.append(tree.words[i-1]) for i in new_order]
	new_tags = []
	[new_tags.append(tree.tags[i-1]) for i in new_order]
	new_heads = []
	[new_heads.append(rev_order[tree.heads[i-1]]) if tree.heads[i-1]!=0 else new_heads.append(0) for i in new_order]
	new_labels = []
	[new_labels.append(tree.labels[i-1]) for i in new_order]
	new_tree = DependencyTree(new_words, new_tags, new_heads, new_labels)
	new_tree.lang_id = tree.lang_id
	new_tree.weight = tree.weight
	return new_tree.conll_str()+'\n\n'

print 'reading ngram trees'
ngram_probs = extract_ngram_probs(os.path.abspath(sys.argv[1]))
print 'reading trees'
t = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[2]))
writer = codecs.open(os.path.abspath(sys.argv[3]),'w')

print 'writing trees'
dropped = 0
count = 0
for tree in t:
	if DependencyTree.is_projective(tree.heads):
		writer.write(reoder_tree(ngram_probs, tree, 100))
	else:
		dropped+=1
	count+=1
	if count%100==0:
		sys.stdout.write(str(count)+'...')
		writer.flush()
		gc.collect()
writer.close()
print 'done!'
print 'dropped', dropped