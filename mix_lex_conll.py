import os,sys,codecs,random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict
from random import randint

'''
	For inserting words to conll file by another language
'''
print 'tree_file output_file [list_of_ngram_files]'

def read_grams(ngram_files):
	unigrams = defaultdict(list)
	for file_path in ngram_files:
		reader = codecs.open(file_path,'r')

		line = reader.readline()
		while line:
			spl = line.strip().split('\t')
			if spl[0] == 'unigram':
				unigrams[spl[1]].append(spl[2])
			line = reader.readline()
	return unigrams

print 'reading trees'
trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')

ngram_files = list()
for i in range(3, len(sys.argv)):
	ngram_files.append(os.path.abspath(sys.argv[i]))

print 'reading ngrams'
unigrams = read_grams(ngram_files)

print 'changing trees'
count =0 
#for tree in trees:
	#writer.write(tree.conll_str()+'\n\n')

for i in range(0,5):
	print i
	for tree in trees:
		effected = False
		t = ['<s>','<s>']+list(tree.tags)+['</s>','</s>']
		for j in range(0, 3):
			r = random.randint(2,len(t)-3)
			dep_context = ' '.join(t[r-2:r+3])
			if unigrams.has_key(dep_context):
				dep_cand= random.randint(0,len(unigrams[dep_context])-1)
				dep_word = unigrams[dep_context][dep_cand]
				tree.words[r-2] = dep_word
				count +=1
				effected = True
		if effected:
			writer.write(tree.conll_str()+'\n\n')
writer.close()
print 'num of inserted words:',count
sys.exit(0)