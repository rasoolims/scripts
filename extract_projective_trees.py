# coding: utf8

import os,sys,codecs
from collections import defaultdict


def show_help():
	print 'python extract_trees.py [input_data] [output_data] '


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


def extract_projective_trees(input_path,output_path):
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
				if is_projective(heads):
					heads=[str(i) for i in heads]
					writer.write('\t'.join(words)+'\n')
					writer.write('\t'.join(tags)+'\n')
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

	sys.stdout.write('\n')
	sys.stdout.flush()


if __name__ == '__main__':
	if len(sys.argv)<3:
		show_help()
		sys.exit(0)
	input_path=os.path.abspath(sys.argv[1])
	output_path=os.path.abspath(sys.argv[2])

	extract_projective_trees(input_path,output_path)
