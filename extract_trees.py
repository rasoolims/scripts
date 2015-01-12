# coding: utf8

import os,sys,codecs
from collections import defaultdict


def show_help():
	print 'python extract_trees.py [min_len] [min_proportion] [input_data] [output_data] [is_labeled]'


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

def has_proportion(heads,min_proportion):
	num=0
	for dep1 in range(1,len(heads)+1):
		if heads[dep1-1]>=0:
			num+=1

	prop=1.0/(len(heads)-1)
	if is_projective(heads) and min_proportion<=prop:
		return True
	return False

def extract_subtree(heads,min_len):
	'''
		extracts indices of words that should be included in the subtree
	'''
	start_index=1
	current_index=1

	spans=set()

	for i in range(1,len(heads)+1):
		for j in range(i+min_len,len(heads)+1):
			use_span=True
			num_of_outs=0
			for k in range(i,j+1):
				if heads[k-1]==-1:
					use_span=False
					break
				if heads[k-1]<i or heads[k-1]>j:
					num_of_outs+=1
				if num_of_outs>1:
					use_span=False
					break
			if use_span:
				for k in range(i,j+1):
					spans.add(k)


	final_heads=list()
	for i in range(1,len(heads)+1):
		head=heads[i-1] if i in spans else -1
		final_heads.append(head)


	return final_heads



def is_full_tree(heads):
	for dep in range(1,len(heads)+1):
		head=heads[dep-1]
		if head==dep or head==-1:
			return False
	return is_projective(heads)


def extract_full_trees(input_path,output_path,min_len,min_proportion,is_labeled):
	trees=defaultdict()
	reader=codecs.open(input_path,'r')
	writer=codecs.open(output_path,'w')
	line=reader.readline()
	words=list()
	tags=list()
	labels=list()
	heads=list()
	counter=0
	while line:
		line=line.strip()
		if not line:
			if len(words)>0:
				sentence=' '.join(words)
				if not trees.has_key(sentence):
					if is_full_tree(heads) or has_proportion(heads,min_proportion):
						trees[sentence]=words,tags,labels,heads
						new_heads=[str(i) for i in heads]
						writer.write('\t'.join(words)+'\n')
						writer.write('\t'.join(tags)+'\n')
						if is_labeled:
							writer.write('\t'.join(labels)+'\n')
						writer.write('\t'.join(new_heads)+'\n\n')
					elif min_len<=len(heads):
						new_heads=extract_subtree(heads,min_len)
						has_subtree=False
						for h in new_heads:
							if h!=-1:
								has_subtree=True
								break
						if has_subtree and is_projective(new_heads):
							heads=[str(i) for i in new_heads]
							writer.write('\t'.join(words)+'\n')
							writer.write('\t'.join(tags)+'\n')
							if is_labeled:
								writer.write('\t'.join(labels)+'\n')
							writer.write('\t'.join(heads)+'\n\n')
				words=list()
				tags=list()
				heads=list()
				labels=list()
				counter+=1
				if counter%10000==0:
					sys.stdout.write(str(counter)+'...')
					sys.stdout.flush()
		elif len(words)==0:
			words=line.split('\t')
		elif len(tags)==0:
			tags=line.split('\t')
		elif len(labels)==0:
			labels=line.split('\t')
		else:
			heads=[int(i) for i in line.split('\t')]
		line=reader.readline()

	sys.stdout.write('\n'+str(len(trees)))
	sys.stdout.write('\n')
	sys.stdout.flush()


if __name__ == '__main__':
	if len(sys.argv)<5:
		show_help()
		sys.exit(0)
	min_len=int(sys.argv[1])
	min_proportion=float(sys.argv[2])
	input_path=os.path.abspath(sys.argv[3])
	output_path=os.path.abspath(sys.argv[4])
	is_labeled=True
	if sys.argv[5]=='false':
		is_labeled=False

	extract_full_trees(input_path,output_path,min_len,min_proportion,is_labeled)
