import os,sys,codecs,random
from collections import defaultdict
from mst_dep_tree_loader import DependencyTree

in_domain_clusters = defaultdict(list)
shared_clusters = defaultdict(str)
possible_tags = defaultdict(set)
lang_words = set()

print 'reading lang tags'
conll_reader = codecs.open(os.path.abspath(sys.argv[1]),'r')
line = conll_reader.readline()
cnt = 0
while line:
	spl = line.strip().split('\t')
	if len(spl)>4:
		possible_tags[spl[1]].add(spl[3])
	else:
		cnt+=1 
		if cnt%10000==0:
			sys.stdout.write(str(cnt)+'...')
	line = conll_reader.readline()

in_domain_cluster_reader = codecs.open(os.path.abspath(sys.argv[2]),'r')
shared_cluster_reader = codecs.open(os.path.abspath(sys.argv[3]),'r')

print '\nreading lang words'
line = in_domain_cluster_reader.readline()
while line:
	spl = line.strip().split('\t')
	if len(spl)>=2:
		lang_words.add(spl[1])

	line = in_domain_cluster_reader.readline()

print 'reading shared clusters'
line = shared_cluster_reader.readline()
while line:
	spl = line.strip().split('\t')
	if len(spl)>=2:
		prefix = spl[0]
		word = spl[1]
		if word in lang_words:
			if not in_domain_clusters.has_key(prefix):
				in_domain_clusters[prefix] = defaultdict(list)
			for tag in possible_tags[word]:
				in_domain_clusters[prefix][tag].append(word)
		shared_clusters[word] = prefix

	line = shared_cluster_reader.readline()

print 'reading trees'
trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[4]))

print 'changing trees...'
replacement_count = 0
cnt = 0
writer = codecs.open(os.path.abspath(sys.argv[5]),'w')
for tree in trees:
	cnt +=1
	if cnt%1000 ==0:
		sys.stdout.write(str(cnt)+'...')
	for i in range(0,len(tree.lemmas)):
		tree.words[i] = '_'
		if tree.tags[i] =='.':
			tree.words[i] = tree.lemmas[i]
		elif shared_clusters.has_key(tree.lemmas[i]):
			prefix = shared_clusters[tree.lemmas[i]]
			if in_domain_clusters.has_key(prefix) and in_domain_clusters[prefix].has_key(tree.tags[i]):
				replacement_candidates = in_domain_clusters[prefix][tree.tags[i]]
				r = random.randint(0,len(replacement_candidates)-1)
				tree.words[i] = replacement_candidates[r]
				replacement_count += 1
	writer.write(tree.conll_str()+'\n\n')

print '\nreplacement count', replacement_count
print 'done'