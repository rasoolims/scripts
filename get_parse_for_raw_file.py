import os,sys,codecs
from mst_dep_tree_loader import DependencyTree

if len(sys.argv)<3:
	print 'python get_parse_for_raw_file.py [reference conll] [raw file] [output file]'
	sys.exit(0)


trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))
src_trees=dict()

for tree in trees:
	sen = ' '.join(tree.words)
	src_trees[sen] = tree

sys.stdout.write('\n')

raw_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
writer=codecs.open(os.path.abspath(sys.argv[3]),'w')

line=raw_reader.readline()
line_count=0
while line:
	line_count+=1
	writer.write(src_trees[line.strip()].tree_str()+'\n\n')
	if line_count%100000==0:
		sys.stdout.write(str(line_count)+'...')
	line=raw_reader.readline()
writer.flush()
writer.close()

