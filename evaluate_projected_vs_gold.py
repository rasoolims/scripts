import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<3:
	print 'python evaluate_projected_vs_gold.py [proj mst] [gold mst]'
	print 'two files do not need to be in the same size/order'
	sys.exit(0)


def is_punc(pos):
	return pos=="#" or pos=="$" or pos=="''" or pos=="(" or pos=="" or pos=="[" or pos=="]" or pos=="{" or pos=="}" or pos=="\"" or pos=="," or pos=="." or pos==":" or pos=="``" or pos=="-LRB-" or pos=="-RRB-" or pos=="-LSB-" or pos=="-RSB-" or pos=="-LCB-" or pos=="-RCB-"



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
		labels=reader.readline()
		hds=reader.readline().strip().split('\t')
		sentence=' '.join(words)

		hs=list()
		for h in hds:
			hs.append(str(int(round(float(h)))))

		hds=hs

		projected_trees[sentence].append([hds,tags])

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

		hs=list()
		for h in hds:
			hs.append(str(int(round(float(h)))))
		hds=hs
		
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
		if gold_trees.has_key(sentence_list):
			gh=gold_trees[sentence_list]
			ph=sentence[0]
			tags=sentence[1]

			is_full=True
			for i in range(0,len(ph)):
				if ph[i]=='-1':
					is_full=False
					break

			l=0
			la=0
			for i in range(0,len(ph)):
				if ph[i]!='-1' and not is_punc(tags[i]):
					all_dep+=1
					la+=1
					if not is_full:
						all_partial+=1
					if ph[i]==gh[i]:
						correct+=1
						if not is_full:
							partial_correct+=1
					else:
						l+=1
			
			if la>0:
				if l>max_change:
					max_change=l
				if l<min_change:
					min_change=l
				change_diag[l]+=1
				avg_change+=l
				all_num+=1
				l=float(l)/la
				local_percent+=l
				if l>max_local_percent:
					max_local_percent=l
				if l<min_local_percent:
					min_local_percent=l
			line_count+=1
			if line_count%100000==0:
				sys.stdout.write(str(line_count)+'...')
sys.stdout.write('\n')

if all_dep==0:
	all_dep=1
accuracy=float(correct)*100.0/all_dep
p_accuracy=0
if all_partial>0:
	p_accuracy=float(partial_correct)*100.0/all_partial
print correct,all_dep
print accuracy
print p_accuracy

local_percent/=all_num

print 'local_percent:',local_percent
print 'min_local_percent:',min_local_percent
print 'max_local_percent:',max_local_percent

avg_change/=all_num
print 'avg_change:',avg_change
print 'min_change:',min_change
print 'max_change:',max_change

print change_diag
