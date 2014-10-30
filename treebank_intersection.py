import os,sys,math,operator,codecs
from collections import defaultdict

def is_full(heads):
	for h in heads:
		if h==-1 or h=='-1':
			return False
	return True

if len(sys.argv)<3:
	print 'python treebank_intersection.py [set_of_treebanks](one or more treebanks) [output_treebank_path]'
	print 'e.g. python treebank_intersection.py fst.mst snd.mst trd.mst output.mst'
	sys.exit(0)

tree_set=defaultdict(list)

for i in range(1,len(sys.argv)-1):
	src_mst_reader=codecs.open(os.path.abspath(sys.argv[i]),'r')

	line=src_mst_reader.readline()
	line_count=0
	while line:
		line=line.strip()
		if line:
			line_count+=1
			words=line.split('\t')
			tags=src_mst_reader.readline().strip().split('\t')
			labels=src_mst_reader.readline().strip().split('\t')
			hds=src_mst_reader.readline().strip().split('\t')
			heads=list()
			for h in hds:
				heads.append(int(round(float(h))))

			tree=[words,tags,labels,heads]
			sentence=' '.join(words)
			if tree_set.has_key(sentence):
				if not is_full(tree_set[sentence][3]):
					if is_full(tree[3]):
						tree_set[sentence][3]=tree[3]
					else:
						for t in range(0,len(tree[3])):
							if not tree_set[sentence][3][t]!=tree[3][t]:
								tree_set[sentence][3][t]=-1
								tree_set[sentence][2][t]='_'
			else:
				tree_set[sentence]=tree
			
			if line_count%100000==0:
				sys.stdout.write(str(line_count)+'...')
				sys.stdout.flush()
		line=src_mst_reader.readline()
	sys.stdout.write(str(line_count)+'\n')
	sys.stdout.flush()

writer=codecs.open(sys.argv[-1],'w')

line_count=0
for sentence in tree_set.keys():
	line_count+=1
	heads=list()
	has_dep=False
	for h in tree_set[sentence][3]:
		if h!=-1:
			has_dep=True
		heads.append(str(h))

	if has_dep:
		writer.write('\t'.join(tree_set[sentence][0])+'\n')
		writer.write('\t'.join(tree_set[sentence][1])+'\n')
		writer.write('\t'.join(tree_set[sentence][2])+'\n')
		writer.write('\t'.join(heads)+'\n\n')

	if line_count%100000==0:
		sys.stdout.write(str(line_count)+'...')
		sys.stdout.flush()	
writer.flush()
writer.close()
sys.stdout.write(str(line_count)+'\ndone\n')
sys.stdout.flush()