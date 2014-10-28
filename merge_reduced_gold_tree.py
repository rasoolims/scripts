import os,sys,math,operator,codecs,traceback
from collections import defaultdict

if len(sys.argv)<4:
	print 'python merge_reduced_gold_tree.py [gold_mst_file] [reduced_mst_file] [output_file_name]'
	print 'the gold trees and merge trees have different orders'
	sys.exit(0)

gold_mst_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
reduced_mst_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
writer=codecs.open(os.path.abspath(sys.argv[3]),'w')

gold_trees=defaultdict()
reduced_trees=defaultdict()


# reading source tree files
sys.stdout.write('reading gold tree files...')
sys.stdout.flush()

line=gold_mst_reader.readline()
line_count=0
while line:
	line=line.strip()
	if line:
		line_count+=1
		words=line.split('\t')
		tags=gold_mst_reader.readline().strip().split('\t')
		labels=gold_mst_reader.readline().strip().split('\t')
		hds=gold_mst_reader.readline().strip().split('\t')

		gold_trees[line_count]=words,tags,labels,hds
		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')
			sys.stdout.flush()
	line=gold_mst_reader.readline()

# reading source tree files
sys.stdout.write('\nreading reduced tree files...')
sys.stdout.flush()

line=reduced_mst_reader.readline()
line_count=0
while line:
	line=line.strip()
	if line:
		line_count+=1
		words=line.split('\t')
		tags=reduced_mst_reader.readline().strip().split('\t')
		labels=reduced_mst_reader.readline().strip().split('\t')
		hds=reduced_mst_reader.readline().strip().split('\t')

		reduced_trees[' '.join(words).strip()]=words,tags,labels,hds
		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')
			sys.stdout.flush()
	line=reduced_mst_reader.readline()

# reading source tree files
sys.stdout.write('\nmapping from reduced tree files...')
sys.stdout.flush()
found=0
for l in gold_trees.keys():
	sen=' '.join(gold_trees[l][0]).strip()
	if reduced_trees.has_key(sen):
		gold_trees[l]=reduced_trees[sen]
		found+=1
	else:
		ln=len(gold_trees[l][0])
		labs=['_']*ln
		hds=['-1']*ln
		gold_trees[l]=gold_trees[l][0],gold_trees[l][1],labs,hds
	writer.write('\t'.join(gold_trees[l][0])+'\n')
	writer.write('\t'.join(gold_trees[l][1])+'\n')
	writer.write('\t'.join(gold_trees[l][2])+'\n')
	writer.write('\t'.join(gold_trees[l][3])+'\n\n')
	if l%100000==0:
		sys.stdout.write(str(l)+'...')
		sys.stdout.flush()
writer.flush()
writer.close()
sys.stdout.write('\ndone with '+str(found)+'!\n')
sys.stdout.flush()