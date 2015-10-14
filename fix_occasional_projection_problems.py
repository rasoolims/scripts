import os,sys,codecs
from collections import defaultdict
from termcolor import colored
from mst_dep_tree_loader import DependencyTree

if len(sys.argv)<5:
	print 'python fix_occasional_projection_problems.py [proj mst] [target_sentences] [gold_src_mst] [intersection-file] [src_map_file] [dst_map_file] [output_file]'
	print 'two files do not need to be in the same size/order'
	sys.exit(0)

def is_punc(pos):
	return pos=="#" or pos=="$" or pos=="''" or pos=="(" or pos=="" or pos=="[" or pos=="]" or pos=="{" or pos=="}" or pos=="\"" or pos=="," or pos=="." or pos==":" or pos=="``" or pos=="-LRB-" or pos=="-RRB-" or pos=="-LSB-" or pos=="-RSB-" or pos=="-LCB-" or pos=="-RCB-"

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


def read_pos_map(path):
	pos_map=defaultdict(str)
	map_reader=open(path,'r')
	line=map_reader.readline()
	while line:
		split_line=line.strip().split('\t')
		if len(split_line)>1:
			pos_map[split_line[0]]=split_line[1]
		line=map_reader.readline()
	return pos_map


projected_trees=defaultdict(list)
line_count=0
reader=codecs.open(os.path.abspath(sys.argv[1]),'r')

line=reader.readline()
while line:
	line=line.strip()
	if line:
		line_count+=1
		words=line.split('\t')
		tags=reader.readline().strip().split('\t')
		labels=reader.readline().strip().split('\t')
		hds=[int(x) for x in reader.readline().strip().split('\t')]
		sentence=' '.join(words)
		projected_trees[sentence].append([words,tags, labels,hds])
	line=reader.readline()

gold_trees=defaultdict()
line_count=0
reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
reader2=codecs.open(os.path.abspath(sys.argv[3]),'r')
reader3=codecs.open(os.path.abspath(sys.argv[4]),'r')

src_pos_map=read_pos_map(os.path.abspath(sys.argv[5]))
dst_pos_map=read_pos_map(os.path.abspath(sys.argv[6]))

writer = codecs.open(os.path.abspath(sys.argv[7]),'w')

line=reader.readline()
line2=reader2.readline()
while line:
	line=line.strip()
	line2=line2.strip()
	if line:
		line3=reader3.readline().strip()
		line_count+=1
		words=line.split(' ')
		words2=line2.split('\t')
		alignment=[-1]*len(words)
		
		try:
			spl=line3.split(' ')
			for x in spl:
				#print x
				spl2=x.split('-')
				s1=int(spl2[0])
				s2=int(spl2[1])
				if s2!=0:
					alignment[s2-1]=s1-1
		except:
			alignment=[-1]*len(words)

		tags2=reader2.readline().strip().split('\t')
		labels2=reader2.readline().strip().split('\t')
		hds2=[int(x) for x in reader2.readline().strip().split('\t')]
		sentence=' '.join(words)

		if not gold_trees.has_key(sentence):
			gold_trees[sentence]=[words2,tags2,labels2,hds2,alignment]

	line=reader.readline()
	line2=reader2.readline()
	line2=reader2.readline()

correct=0
all_dep=0
line_count=0

all_partial=0
partial_correct=0

local_percent=0.0
all_num=0
max_local_percent=0.0
min_local_percent=1.0
min_change=10000
max_change=0
avg_change=0.0
change_diag=defaultdict(int)

for sentence_list in projected_trees.keys():
	for sentence in projected_trees[sentence_list]:
		proj_words = sentence[0]
		proj_tags = sentence[1]
		proj_labels = sentence[2]
		proj_heads = sentence[3]
		projected_tree = DependencyTree(proj_words,proj_tags,proj_heads,proj_labels)

		source_words = gold_trees[sentence_list][0]
		source_tags = gold_trees[sentence_list][1]
		source_labels = gold_trees[sentence_list][2]
		source_heads = gold_trees[sentence_list][3]
		alignment = gold_trees[sentence_list][4]
		source_tree = DependencyTree(source_words,source_tags,source_heads,source_labels)

		change_list = list()

		for i in range(0, len(proj_tags)):
			if proj_tags[i] == 'VERB' and proj_heads[i]>0 and proj_tags[proj_heads[i]-1]=='VERB':
				mod_aligned_index = alignment[i]
				head_aligned_index = alignment[proj_heads[i]-1]

				# fix auxiliary problem
				has_target_aux = False
				has_source_aux = False

				for m in projected_tree.reverse_tree[i+1]:
					if proj_labels[m-1]=='aux':
						has_target_aux = True
						break

				if has_target_aux:
					continue

				for m in source_tree.reverse_tree[mod_aligned_index+1]:
					if source_labels[m-1]=='aux':
						has_source_aux = True
						break

				if not has_source_aux:
					continue

				change_list.append([i,proj_heads[i]-1])
				


		for change in change_list:
			print '->->->->->->->'
			mod = change[0]
			head = change[1]

			new_heads = list()

			for h in range(0,len(proj_heads)):
				new_heads.append(proj_heads[h])

			
			for h in range(0,len(proj_heads)):
				if h==mod or h==head:
					continue
				if proj_heads[h] == head + 1:
					new_heads[h] = mod + 1
					print '^^^^^^^^^^^^'
					print proj_heads
					print new_heads
				#if not is_projective(new_heads):
					#print 'not projective'
					#new_heads[h] = proj_heads[h]

			new_heads[mod] = proj_heads[head]
			new_heads[head] = mod + 1
			print '?????????????'
			print proj_heads
			print new_heads

			if not is_projective(new_heads):
				print 'not projective'
				continue

			proj_heads = new_heads

		writer.write('\t'.join(proj_words)+'\n')
		writer.write('\t'.join(proj_tags)+'\n')
		writer.write('\t'.join(proj_labels)+'\n')
		writer.write('\t'.join((str(x) for x in proj_heads))+'\n\n')

writer.close()

print 'done!'

