import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<4:
	print 'python extract_equivalant_gold_trees.py [proj mst] [gold mst] [dst_file]'
	print 'two files do not need to be in the same size/order'
	sys.exit(0)


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
		hs=list()

		for h in hds:
			hs.append(str(int(round(float(h)))))

		sentence=' '.join(words)

		if not gold_trees.has_key(sentence):
			gold_trees[sentence]='\t'.join(hs)
			gold_tree_labs[sentence]=labels

		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')

	line=reader.readline()
sys.stdout.write('\n')

writer=codecs.open(os.path.abspath(sys.argv[3]),'w')

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
		hds=reader.readline().strip()
		sentence=' '.join(words)

		if gold_tree_labs.has_key(sentence):
			labels=gold_tree_labs[sentence]
			hds=gold_trees[sentence]

		writer.write('\t'.join(words)+'\n')
		writer.write('\t'.join(tags)+'\n')
		writer.write(labels+'\n')
		writer.write(hds+'\n\n')


		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')

	line=reader.readline()
sys.stdout.write('\n')


writer.flush()
writer.close()
