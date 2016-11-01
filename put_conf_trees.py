import os,sys,codecs,random,math
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict
from random import randint

if len(sys.argv)<4:
	print 'source_conll_file conll_file output_file'
	sys.exit(0)


print 'reading target trees'

t = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))

print 'estimating probabilities'
bigram_count = defaultdict(int)
trigram_count = defaultdict(float)
for tree in t:
	tags = ['<s>'] +tree.tags +['</s>']

	for i in range(0, len(tags)-2):
		bigram = tags[i]+' '+tags[i+1]
		trigram = bigram+' '+tags[i+2]

		bigram_count[bigram]+=1
		trigram_count[trigram]+=1.0

for trigram in trigram_count.keys():
	bigram = trigram.split(' ')[0]+' '+trigram.split(' ')[1]
	trigram_count[trigram]=trigram_count[trigram]/bigram_count[bigram]
small_value = 1e-20

print 'reading trees'
t = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[2]))

print 'writing trees'
writer = codecs.open(os.path.abspath(sys.argv[3]),'w')

c = 0
v = 0
for i in range(len(t)):
	if len(t[i].tags)<2 or  not DependencyTree.is_projective(t[i].heads):
		continue
	v += 1
	tags = ['<s>'] +t[i].tags +['</s>']
	prob = 0.0
	for j in range(0, len(tags)-2):
		trigram = tags[j]+' '+tags[j+1] +' '+tags[j+2]
		if not trigram_count.has_key(trigram):
			trigram_count[trigram] = small_value
		prob+= math.log(trigram_count[trigram])
	prob = math.exp(prob/len(t[i].tags))
	t[i].weight = prob
	writer.write(t[i].conll_str()+'\n\n')
	c+= 1
	if c%10000==0:
		sys.stdout.write(str(c)+'...')
sys.stdout.write(str(c)+'\n')
print v
writer.close()
