import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<3:
	print 'python evaluate_projected_vs_gold.py [proj mst] [gold mst]'
	print 'two files do not need to be in the same size/order'
	sys.exit(0)


def is_punc(pos):
	return pos=="#" or pos=="$" or pos=="''" or pos=="(" or pos=="" or pos=="[" or pos=="]" or pos=="{" or pos=="}" or pos=="\"" or pos=="," or pos=="." or pos==":" or pos=="``" or pos=="-LRB-" or pos=="-RRB-" or pos=="-LSB-" or pos=="-RSB-" or pos=="-LCB-" or pos=="-RCB-"



projected_trees=defaultdict()
line_count=0
reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
line=reader.readline()
while line:
	line=line.strip()
	if line:
		line_count+=1
		words=line.split('\t')
		tags=reader.readline().strip().split('\t')
		labels=reader.readline()
		hds=reader.readline().strip().split('\t')
		sentence=' '.join(words)

		if not projected_trees.has_key(sentence):
			projected_trees[sentence]=[hds,tags]

		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')

	line=reader.readline()
sys.stdout.write('\n')


gold_trees=defaultdict()
line_count=0
reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
line=reader.readline()
while line:
	line=line.strip()
	if line:
		line_count+=1
		words=line.split('\t')
		tags=reader.readline()
		labels=reader.readline()
		hds=reader.readline().strip().split('\t')
		sentence=' '.join(words)

		if not gold_trees.has_key(sentence):
			gold_trees[sentence]=hds

		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')

	line=reader.readline()
sys.stdout.write('\n')


correct=0
all_dep=0
line_count=0

all_partial=0
partial_correct=0

for sentence in projected_trees.keys():
	if gold_trees.has_key(sentence):
		gh=gold_trees[sentence]
		ph=projected_trees[sentence][0]
		tags=projected_trees[sentence][1]

		is_full=True
		for i in range(0,len(ph)):
			if ph[i]=='-1':
				is_full=False
				break

		for i in range(0,len(ph)):
			if ph[i]!='-1' and not is_punc(tags[i]):
				all_dep+=1
				if not is_full:
					all_partial+=1
				if ph[i]==gh[i]:
					correct+=1
					if not is_full:
						partial_correct+=1
		line_count+=1
		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')
sys.stdout.write('\n')

accuracy=float(correct)*100.0/all_dep
p_accuracy=0
if all_partial>0:
	p_accuracy=float(partial_correct)*100.0/all_partial
print correct,all_dep
print accuracy
print p_accuracy

