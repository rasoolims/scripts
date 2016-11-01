import os,sys,codecs,random,math
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict
from random import randint

if len(sys.argv)<5:
	print 'source_conll_file conll_file output_file max_num'
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
max_num = int(sys.argv[4])

c = 0
seen = set()
v = 0
while True:
	i = random.randint(0,len(t)-1)
	v += 1
	if (not i in seen) and DependencyTree.is_projective(t[i].heads) and len(t[i].tags)>1:
		seen.add(i)
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
		if c%1000==0:
			sys.stdout.write(str(c)+'...')
	if c>= max_num:
		break
sys.stdout.write(str(c)+'\n')
print v
writer.close()
