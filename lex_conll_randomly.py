import os,sys,codecs,random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict
from random import randint

def read_grams(file_path):
	reader = codecs.open(file_path,'r')
	bigrams = defaultdict(list)
	trigrams = defaultdict(list)

	line = reader.readline()
	while line:
		spl = line.strip().split('\t')
		if spl[0]=='bigram':
			bigrams[spl[1]].append(spl[2])
		elif spl[0] == 'trigram':
			trigrams[spl[1]].append(spl[2])
		line = reader.readline()
	print len(bigrams)
	print len(trigrams)
	return [bigrams,trigrams]

trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
x_pair = read_grams(os.path.abspath(sys.argv[2]))
bigrams = x_pair[0]
trigrams = x_pair[1]
writer =  codecs.open(os.path.abspath(sys.argv[3]),'w')

for tree in trees:
	t = ['<s>']+list(tree.tags)+['</s>']
	b = 0 # random.randint(0,1)

	lex_set = set()

	for i in range(0,1):
		if b ==1 and len(t)>4:
			r = random.randint(1,len(t)-4)

			should_add = True
			for j in range(r,r+3):
				if r in lex_set:
					should_add = False
					break

			if not should_add:
				continue

			trigram_context = ' '.join(t[r-1:r+4])

			for j in range(r,r+3):
				lex_set.add(r)

			candidates = trigrams[trigram_context]
			if len(candidates)>0:
				r2 = random.randint(0,len(candidates)-1)

				candidate = candidates[r2].split(' ')

				tree.words[r-1]=candidate[0]
				tree.words[r]=candidate[1]
				tree.words[r+1]=candidate[2]
			else:
				print 'no trigram context',trigram_context
		elif len(t)>3:
			r = random.randint(1,len(t)-3)

			should_add = True
			for j in range(r,r+2):
				if r in lex_set:
					should_add = False
					break

			if not should_add:
				continue

			bigram_context = ' '.join(t[r-1:r+3])

			for j in range(r,r+2):
				lex_set.add(r)

			candidates = bigrams[bigram_context]
			if len(candidates)>0:
				r2 = random.randint(0,len(candidates)-1)

				candidate = candidates[r2].split(' ')

				tree.words[r-1]=candidate[0]
				tree.words[r]=candidate[1]
			else:
				print 'no bigram context',bigram_context


	writer.write(tree.conll_str()+'\n\n')