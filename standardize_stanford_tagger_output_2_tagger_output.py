import os,sys
from collections import defaultdict

def read_pos_map(path):
	pos_map=defaultdict(str)
	map_reader=open(path,'r')
	line=map_reader.readline()
	while line:
		split_line=line.strip().split('\t')
		if len(split_line)>1:
			pos_map[split_line[0]]=split_line[1]
		line=map_reader.readline()
	return pos_map


def normalizeWords(fields):
	if fields=="-LRB-":
		fields = "(";
	elif fields=="-RRB-":
		fields = ")";
	elif fields=="-LCB-":
		fields = "{";
	elif fields=="-RCB-":
		fields = "}";
	elif fields=="-LSB-":
		fields = "[";
	elif fields=="-RSB-":
		fields = "]";
	return fields

if len(sys.argv)<3:
	print 'python standardize_stanford_tagger_output_2_tagger_output.py pos_map_file tag_file output_file'
	sys.exit(0)


pos_map=read_pos_map(os.path.abspath(sys.argv[1]))

reader=open(os.path.abspath(sys.argv[2]),'r')
writer=open(os.path.abspath(sys.argv[3]),'w')
line=reader.readline()
counter=0
while line:
	tokens=line.strip().split(' ')
	words=list()

	for tok in tokens:
		word=tok[:tok.rfind('_')]
		tag=tok[tok.rfind('_')+1:]
		word=normalizeWords(word)
		if pos_map.has_key(tag):
			tag=pos_map[tag]
		words.append(word+'_'+tag)
	writer.write(' '.join(words)+'\n')
	counter+=1
	if counter%10000==0:
		sys.stdout.write(str(counter)+'...')
		sys.stdout.flush()
	line=reader.readline()
writer.flush()
writer.close()
sys.stdout.write('\n')