# coding: utf8

import os,sys,codecs
from collections import defaultdict


def is_dense(heads, most_empty_span):
	mx=0
	m=0
	for h in heads:
		if h==-1:
			m+=1
		else:
			if m>mx:
				mx=m
			m=0
	if m>mx:
		mx=m

	if mx<=most_empty_span:
		return True
	return False

def extract_dense_trees(input_path,output_path,most_empty_span):
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
				if is_dense(heads,most_empty_span):
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
	most_empty_span=int(sys.argv[3])

	extract_dense_trees(input_path,output_path,most_empty_span)


