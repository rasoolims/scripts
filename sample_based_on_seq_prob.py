import os,sys,codecs,random,math,operator
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict
from random import randint

if len(sys.argv)<4:
	print 'conll_file output_file max_num'
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


print 'reading source trees'
s = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[2]))


small_value = 1e-20

print 'tree prob estimation for source sentences'
prob_tree_dic = defaultdict(list)
for i in range(0,len(s)):
	if i%1000 ==0:
		sys.stdout.write(str(i)+'...')
	if not DependencyTree.is_projective(s[i].heads):
		continue

	tags = ['<s>'] +s[i].tags +['</s>']
	prob = 0.0
	for j in range(0, len(tags)-2):
		trigram = tags[j]+' '+tags[j+1] +' '+tags[j+2]

		if not trigram_count.has_key(trigram):
			trigram_count[trigram] = small_value
		prob+= math.log(trigram_count[trigram])

	prob = math.exp(prob)
	s[i].weight = prob

	prob_tree_dic[prob].append(s[i])
sys.stdout.write('\n')

print 'sorting based on likelihood'
sorted_list = prob_tree_dic.keys()
sorted_list.sort(reverse=True)

print 'writing most likely trees'
max_num = int(sys.argv[3])
writer = codecs.open(os.path.abspath(sys.argv[4]),'w')

c = 0
for s in sorted_list:
	for t in prob_tree_dic[s]:
		c+=1
		if c%100==0:
			sys.stdout.write(str(s)+'...')
		writer.write(t.conll_str()+'\n\n')
		if c>=max_num:
			break
	if c>=max_num:
		break

writer.close()
print 'done!'


