import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<4:
	print 'python extract_max_vote_dep_projection.py [list of projected_tree mst files] [min_vote] [output]'
	sys.exit(0)

projected_trees=defaultdict()
min_vote=int(sys.argv[-2])

writer=codecs.open(os.path.abspath(sys.argv[-1]),'w')

for i in range(1,len(sys.argv)-2):
	line_count=0
	reader=codecs.open(os.path.abspath(sys.argv[i]),'r')
	line=reader.readline()
	while line:
		line=line.strip()
		if line:
			line_count+=1
			words=line.split('\t')
			tags=reader.readline().strip().split('\t')
			labels=reader.readline().strip().split('\t')
			hds=reader.readline().strip().split('\t')

			sentence=' '.join(words)

			if not projected_trees.has_key(sentence):
				projected_trees[sentence]=list()
				projected_trees[sentence].append(words)
				projected_trees[sentence].append(tags)

			projected_trees[sentence].append(hds)

			if line_count%100000==0:
				sys.stdout.write(str(line_count)+'...')

		line=reader.readline()
	sys.stdout.write('\n')

line_count=0
all_possib=0
projected=0
for sentence in projected_trees.keys():
	words=projected_trees[sentence][0]
	tags=projected_trees[sentence][1]

	max_vote_heads=list()

	for i in range(0,len(tags)):
		head_votes=defaultdict(int)
		for j in range(2,len(projected_trees[sentence])):
			h=projected_trees[sentence][j][i]
			if h!='-1':
				head_votes[h]+=1

		max_vote=0
		max_h=0
		for h in head_votes.keys():
			if head_votes[h]>max_vote:
				max_vote=head_votes[h]
				max_h=h

		all_possib+=1
		if max_vote>=min_vote:
			projected+=1
			max_vote_heads.append(max_h)
		else:
			max_vote_heads.append('-1')

	writer.write('\t'.join(words)+'\n')
	writer.write('\t'.join(tags)+'\n')
	writer.write('\t'.join(['_']*len(tags))+'\n')
	writer.write('\t'.join(max_vote_heads)+'\n\n')
	line_count+=1
	if line_count%100000==0:
		sys.stdout.write(str(line_count)+'...')

writer.flush()
writer.close()
sys.stdout.write('\n')
print projected,all_possib
