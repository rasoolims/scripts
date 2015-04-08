import sys,os,codecs,operator,random
from collections import defaultdict


brown_cluster_set=defaultdict(set)
brown_cluster=defaultdict(list)
rev_brown_cluster=defaultdict(str)
breader=codecs.open(os.path.abspath(sys.argv[1]),'r')
line=breader.readline()
while line:
	spl=line.strip().split()
	if len(spl)>2:
		brown_cluster_set[spl[0]].add(spl[1])
		rev_brown_cluster[spl[1]]=spl[0]
	line=breader.readline()

for x in brown_cluster_set.keys():
	brown_cluster[x]=list()
	for y in brown_cluster_set[x]:
		brown_cluster[x].append(y)
print len(brown_cluster)

train_sens=codecs.open(os.path.abspath(sys.argv[2]),'r').read().split('\n')
writer=codecs.open(sys.argv[3],'w')

sen_set=set()
for sen in train_sens:
	if sen.strip():
		sen_set.add(sen.strip())

for i in range(0,10):
	print i
	for sen in train_sens:
		words=list()
		tags=list()
		for s in sen.strip().split(' '):
			try:
				if len(s.split('_'))==2:
					words.append(s.split('_')[0])
					tags.append(s.split('_')[1])
			except:
				print s

		if len(words)==0:
			continue

		r=random.randint(0,len(words)-1)

		if rev_brown_cluster.has_key(words[r]):
			c=rev_brown_cluster[words[r]]
			r2=random.randint(0,len(brown_cluster[c])-1)
			replacement=brown_cluster[c][r2]
			words[r]=replacement

		final_sen=list()
		for i in range(0,len(words)):
			final_sen.append(words[i]+'_'+tags[i])

		sen_set.add(' '.join(final_sen))

writer.write('\n'.join(sen_set))
writer.flush()
