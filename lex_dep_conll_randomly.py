import os,sys,codecs,random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict
from random import randint

def read_grams(file_path):
	reader = codecs.open(file_path,'r')
	bigrams = defaultdict(list)
	trigrams = defaultdict(list)
	unigrams = defaultdict(list)

	line = reader.readline()
	while line:
		spl = line.strip().split('\t')
		if spl[0]=='bigram':
			bigrams[spl[1]].append(spl[2])
		elif spl[0] == 'trigram':
			trigrams[spl[1]].append(spl[2])
		elif spl[0] == 'unigram':
			unigrams[spl[1]].append(spl[2])
		line = reader.readline()
	print len(bigrams)
	print len(trigrams)
	return [bigrams,trigrams,unigrams]

trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
x_pair = read_grams(os.path.abspath(sys.argv[2]))
bigrams = x_pair[0]
trigrams = x_pair[1]
unigrams = x_pair[2]

writer =  codecs.open(os.path.abspath(sys.argv[3]),'w')

for tree in trees:
	t = ['<s>','<s>']+list(tree.tags)+['</s>','</s>']
	b = 0 # random.randint(0,1)

	lex_set = set()

	for i in range(0,1):
		r = random.randint(2,len(t)-3)
		dep_context = ' '.join(t[r-1:r+4])

		head = tree.heads[r-2]

		if head>0:
			#print head, len(t)
			head_context = ' '.join(t[head-1:head+4])
			#print t
			#print head
			#print head_context

			if unigrams.has_key(head_context) and unigrams.has_key(dep_context):
				head_cand = random.randint(0,len(unigrams[head_context])-1)
				head_word = unigrams[head_context][head_cand]

				dep_cand= random.randint(0,len(unigrams[dep_context])-1)
				dep_word = unigrams[dep_context][dep_cand]
				tree.words[r-2] = dep_word
				tree.words[head-1] = head_word
			#else:
				#print '--> found',head_context,'=======',dep_context
			else:
				print 'not found',head_context,'=======',dep_context


	writer.write(tree.conll_str()+'\n\n')