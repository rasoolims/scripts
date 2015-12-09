import codecs,os,sys,math,operator, random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict

print 'reading trees'
gold_trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
parsed_trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[2]))

trigram_counts = defaultdict(int)
bigram_counts = defaultdict(int)
probs = defaultdict(float)

training_bigram_counts = defaultdict(int)
training_trigram_count = defaultdict(int)
training_probs = defaultdict(int)

weight = int(sys.argv[4])

print 'calculate lm'
for tree in gold_trees:
	tags = ['<s>','<s>']+tree.tags+['</s>']

	for i in range(2, len(tags)):
		trigram = ' '.join(tags[i-2:i+1])
		bigram = ' '.join(tags[i-2:i])

		trigram_counts[trigram]+=1
		bigram_counts[bigram]+=1


# create target language distribution
for trigram in trigram_counts.keys():
	bigram = ' '.join(trigram.split(' ')[:2])
	probs[trigram] = float(trigram_counts[trigram])/bigram_counts[bigram]

remained_sens = set(range(0, len(gold_trees)))
added_trees = set()
kl_dict = defaultdict()

print 'greed search'
for it in range(0, 50):
	sys.stdout.write(str(it)+'...')
	selected = random.randint(0, len(gold_trees))
	if it > 0:
		min_kl = float('inf')
		selected = 0

		for j in remained_sens:
			tags = ['<s>','<s>']+gold_trees[j].tags+['</s>']
			kl = 0

			tc = defaultdict(int)
			bc = defaultdict(int)
			for i in range(2, len(tags)):
				trigram = ' '.join(tags[i-2:i+1])
				bigram = ' '.join(tags[i-2:i])
				tc[trigram]+=1
				bc[bigram]+=1

			for trigram in tc.keys():
				bigram = ' '.join(trigram.split(' ')[:2])
				q_tr_count = tc[trigram] 
				if  training_trigram_count.has_key(trigram):
					q_tr_count += training_trigram_count[trigram]
				q_b_count = bc[bigram]
				if  training_bigram_counts.has_key(bigram):
					q_tr_count += training_bigram_counts[bigram] 
				q = float(q_tr_count)/q_b_count
				kl += probs[trigram]*(math.log(probs[trigram]) - math.log(q))

			for trigram in training_probs.keys():
				if tc.has_key(trigram):
					continue
				q = training_probs[trigram]
				kl += probs[trigram]*(math.log(probs[trigram]) - math.log(q))

			if kl < min_kl:
				min_kl = kl
				selected = j 

	tags = ['<s>','<s>']+gold_trees[selected].tags+['</s>']
	for i in range(2, len(tags)):
		trigram = ' '.join(tags[i-2:i+1])
		bigram = ' '.join(tags[i-2:i])
		training_trigram_count[trigram] += 1
		training_bigram_counts[bigram] += 1

	for trigram in training_trigram_count.keys():
		bigram = ' '.join(trigram.split(' ')[:2])
		try:
			training_probs[trigram] =  float(training_trigram_count[trigram])/training_bigram_counts[bigram]
		except:
			print bigram
			print trigram
			print training_trigram_count[trigram]
			sys.exit(1)

	remained_sens.remove(selected)


print '\nwriting'

writer1 = codecs.open(os.path.abspath(sys.argv[3])+'.active.gold.conll','w')
writer2 = codecs.open(os.path.abspath(sys.argv[3])+'.active.auto.conll','w')
writer3 = codecs.open(os.path.abspath(sys.argv[3])+'.auto.gold.conll','w')
writer4 = codecs.open(os.path.abspath(sys.argv[3])+'.auto.auto.conll','w')

for i in range(0, len(gold_trees)):
	if i in remained_sens:
		writer4.write(parsed_trees[i].conll_str()+'\n\n')
		writer3.write(gold_trees[i].conll_str()+'\n\n')
	else:
		parsed_trees[i].weight = weight
		gold_trees[i].weight = weight
		writer2.write(parsed_trees[i].conll_str()+'\n\n')
		writer1.write(gold_trees[i].conll_str()+'\n\n')

writer1.close()
writer2.close()
writer3.close()
writer4.close()
print 'done'





