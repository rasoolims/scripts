import os,sys,codecs
from collections import defaultdict

def is_punc(pos):
	return pos=="#" or pos=="$" or pos=="''" or pos=="(" or pos=="" or pos=="[" or pos=="]" or pos=="{" or pos=="}" or pos=="\"" or pos=="," or pos=="." or pos==":" or pos=="``" or pos=="-LRB-" or pos=="-RRB-" or pos=="-LSB-" or pos=="-RSB-" or pos=="-LCB-" or pos=="-RCB-"



if len(sys.argv)<4:
	print 'python extract_accurate_projected_vs_gold.py [proj mst] [gold mst] [max_num] [dst_file]'
	print 'two files do not need to be in the same size/order'
	sys.exit(0)

max_num=int(sys.argv[3])

gold_trees=defaultdict()
gold_tree_labs=defaultdict()
line_count=0
reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
line=reader.readline()
while line:
	line=line.strip()
	if line:
		line_count+=1
		words=line.split('\t')
		tags=reader.readline().strip()
		labels=reader.readline().strip()
		hds=reader.readline().strip().split('\t')
		
		sentence=' '.join(words)

		gold_trees[sentence]=hds
		gold_tree_labs[sentence]=labels

		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')

	line=reader.readline()
sys.stdout.write('\n')

writer=codecs.open(os.path.abspath(sys.argv[4]),'w')

line_count=0
reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
line=reader.readline()
while line:
	line=line.strip()
	if line:
		line_count+=1
		words=line.split('\t')
		tags=reader.readline().strip().split('\t')
		labels=reader.readline().strip()
		hds=reader.readline().strip().split('\t')
		sentence=' '.join(words)

		l=0
		if gold_trees.has_key(sentence):
			ghds=gold_trees[sentence]
			for i in range(0,len(hds)):
				if hds[i]!=ghds[i]:
					if not is_punc(tags[i]):
						l+=1



			if l<=max_num:
				writer.write('\t'.join(words)+'\n')
				writer.write('\t'.join(tags)+'\n')
				writer.write(labels+'\n')
				writer.write('\t'.join(hds)+'\n\n')

		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')

	line=reader.readline()
sys.stdout.write('\n')


writer.flush()
writer.close()
