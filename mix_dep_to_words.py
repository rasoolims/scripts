import os,sys,codecs,random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict

context_grams = defaultdict(list)

reader = codecs.open(os.path.abspath(sys.argv[1]),'r')
line = reader.readline()
while line:
	spl = line.strip().split('\t')
	if len(spl)>1:
		context_grams[spl[0]].append(spl[1])

	line = reader.readline()

trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[2]))

writer = codecs.open(os.path.abspath(sys.argv[3]),'w')

cnt = 0
for tree in trees:
	t = ['<s>','<s>']+list(tree.tags)+['</s>','</s>']
	
	replaced_words = dict()
	for i in range(0,len(tree.tags)):
		child_context = t[i+1]+' '+t[i+2]+' '+t[i+3]
		cw = tree.words[i]
		h = tree.heads[i]
		head_context = '_ ROOT _'
		hw = 'ROOT'
		if h>0:
			hw = tree.words[h-1]
			head_context = t[h]+' '+t[h+1]+' '+t[h+2]
		else:
			continue
		rel = tree.labels[i]

		context = rel +' '+child_context +' '+head_context

		if context_grams.has_key(context):
			r = random.randint(0,len(context_grams[context])-1)
			spl_words = context_grams[context][r].split(' ')

			replaced_words[i] = spl_words[0]
			if h>0:
				replaced_words[h-1] = spl_words[1]

	for i in replaced_words.keys():
		tree.words[i] = replaced_words[i]

	for i in range(0,len(tree.tags)):
		tree.lemmas[i] = '_'

	writer.write(tree.conll_str()+'\n\n')
	cnt +=1
	if cnt%100 == 0:
		sys.stdout.write(str(cnt)+'...')
writer.close()
sys.stdout.write(str(cnt)+'\n')



