import os,sys,codecs,random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict

def same_pos_kind(p1,p2):
	if p1==p2:
		return True
	
	if p1 == 'PUNCT':
		p1 = '.'
	if p2 == 'PUNCT':
		p2 = '.'

	if p1=='PRON':
		if p2=='DET' or p2=='NOUN' or p2=='ADJ':
			return True
	if p1=='NOUN':
		if p2=='DET' or p2=='PRON':
			return True
	if p1=='DET':
		if p2=='NOUN' or p2=='PRON' or p2=='NUM':
			return True;
	if p1=='PRT':
		if p2=='ADV':
			return True
	if p1=='ADV':
		if p2=='PRT' or p2=='ADJ':
			return True
	if p1=='ADJ':
		if p2=='ADV' or p2=='PRON':
			return True
	if p1=='X':
		if p2=='NUM' or p2=='.':
			return True
	if p1=='.':
		if p2=='X':
			return True
	if p1=='NUM':
		if p2=='X' or p2=='DET':
			return True

	return False


r1 = codecs.open(os.path.abspath(sys.argv[1]),'r')
r2 = codecs.open(os.path.abspath(sys.argv[2]),'r')
ar = codecs.open(os.path.abspath(sys.argv[3]),'r')
writer = codecs.open(os.path.abspath(sys.argv[4]),'w')
l1 = r1.readline()
while l1:
	l2 = r2.readline()
	src_tags = []
	dst_tags = []
	for tok in l1.strip().split():
		src_tags.append(tok[tok.rfind('_')+1:])
	for tok in l2.strip().split():
		dst_tags.append(tok[tok.rfind('_')+1:])

	alignments = ar.readline().strip().split()
	
	final_alignments = []
	for align in alignments:
		a,b = align.split('-')
		if same_pos_kind(src_tags[int(a)],dst_tags[int(b)]):
			final_alignments.append(align)
	writer.write(' '.join(final_alignments)+'\n')

	l1 = r1.readline()

