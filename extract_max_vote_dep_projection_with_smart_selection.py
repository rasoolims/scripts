import os,sys,codecs,operator
from collections import defaultdict


def trav(rev_head,h,visited):
	if rev_head.has_key(h):
		for d in rev_head[h]:
			if d in visited:
				return True
			visited.append(d)
			trav(rev_head,d,visited)
	return False

def is_full(heads):
	for dep1 in range(1,len(heads)+1):
		head1=heads[dep1-1]
		if head1<0:
			return False
	return True

def is_projective(heads):
	rev_head=defaultdict(list)
	for dep1 in range(1,len(heads)+1):
		head1=heads[dep1-1]
		if head1>=0:
			rev_head[head1].append(dep1)

	visited=list()
	#print rev_head
	if trav(rev_head,0,visited):
		return False
	if len(visited)<len(heads) and is_full(heads):
		return False

	rootN=0
	for dep1 in range(1,len(heads)+1):
		head1=heads[dep1-1]

		if rev_head.has_key(dep1):
			for d2 in rev_head[dep1]:
				if (d2<head1 and head1<dep1) or (d2>head1 and head1>dep1) and head1>0:
					return False

		if head1==0:
			rootN+=1
		for dep2 in range(1,len(heads)+1):
			head2=heads[dep2-1]
			if head1==-1 or head2==-1:
				continue
			if dep1>head1 and head1!=head2:
				if dep1>head2 and dep1<dep2 and head1<head2:
					return False
				if dep1<head2 and dep1>dep2 and head1<dep2:
					return False
			if dep1<head1 and head1!=head2:
				if head1>head2 and head1<dep2 and dep1<head2:
					return False
				if head1<head2 and head1>dep2 and dep1<dep2:
					return False
	if rootN!=1:
		return False
	return True
##################################################################################################################################
if len(sys.argv)<4:
	print 'python extract_max_vote_dep_projection.py [list of projected_tree mst files] [min_vote] [output]'
	sys.exit(0)
##################################################################################################################################

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

			projected_trees[sentence].append([hds,labels])

			if line_count%100000==0:
				sys.stdout.write(str(line_count)+'...')

		line=reader.readline()
	sys.stdout.write('\n')

line_count=0
for sentence in projected_trees.keys():
	words=projected_trees[sentence][0]
	tags=projected_trees[sentence][1]

	curr_heads=list()
	curr_labels=list()

	max_vote_heads=list()
	max_vote_labs=list()
	vote_num=defaultdict()
	for i in range(0,len(tags)):
		curr_heads.append(-1)
		curr_labels.append('_')

		vote_num[i]=defaultdict(int)
		for j in range(2,len(projected_trees[sentence])):
			h=projected_trees[sentence][j][0][i]
			l=projected_trees[sentence][j][1][i]
			vote_num[i][h+'#'+l]+=1

	remaining_votes=set()
	sorted_dict=defaultdict()
	for  i in range(0,len(tags)):
		remaining_votes.add(i)
		sorted_dict[i] = sorted(vote_num[i].items(), key=operator.itemgetter(1),reverse=True)
	while True:
		if len(remaining_votes)==0:
			break

		best_vote=-1
		max_vote=-100000
		for i in remaining_votes:
			if len(vote_num[i])==0:
				continue
			m=sorted_dict[i][0][1]
			if m>max_vote:
				max_vote=m

		if best_vote==-1:
			break

		h=int(max_vote[:max_vote.find('#')])
		l=max_vote[max_vote.find('#')+1:]

		curr_heads[best_vote]=h
		if is_projective(curr_heads):
			remaining_votes.remove(best_vote)
			curr_labels[best_vote]=l
		else:
			del vote_num[best_vote][max_vote]
			curr_heads[best_vote]=-1
			if len(vote_num[best_vote])>0:
				sorted_dict[best_vote] = sorted(vote_num[best_vote].items(), key=operator.itemgetter(1),reverse=True)

	
	final_heads=[str(i) for i in curr_heads]

	writer.write('\t'.join(words)+'\n')	
	writer.write('\t'.join(tags)+'\n')	
	writer.write('\t'.join(curr_labels)+'\n\n')	
	writer.write('\t'.join(final_heads)+'\n')	

	line_count+=1
	if line_count%100000==0:
		sys.stdout.write(str(line_count)+'...')

writer.flush()
writer.close()
sys.stdout.write('\n')
