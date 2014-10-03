import os,sys
from collections import defaultdict

def read_pos_map(path):
	pos_map=defaultdict(str)
	map_reader=open(path,'r')
	line=map_reader.readline()
	while line:
		split_line=line.split('\t')
		if len(split_line)>1:
			pos_map[split_line[0]]=split_line[1]
		line=map_reader.readline()
	return pos_map

def normalizeWords(fields):
	if fields[1]=="-LRB-":
		fields[1] = "(";
	elif fields[1]=="-RRB-":
		fields[1] = ")";
	elif fields[1]=="-LCB-":
		fields[1] = "{";
	elif fields[1]=="-RCB-":
		fields[1] = "}";
	elif fields[1]=="-LSB-":
		fields[1] = "[";
	elif fields[1]=="-RSB-":
		fields[1] = "]";
	return fields


def normalize_tags(fields):
	if fields[3]=="-LRB-":
			fields[3] = "(";
	elif fields[3]=="-RRB-":
		fields[3] = ")";
	elif fields[3]=="TO" and fields[1].lower()=="to":
		fields[3] = "IN";
	if fields[3]=="IN" and fields[1].lower()=="to" and (fields[7]=="aux" or fields[7]=="xcomp" or fields[7]=="ccomp"):
		fields[3] = "TO";
	return fields

def normalize_labels(fields):
	if fields[7]=="null":
			fields[7] = "ROOT";
	elif fields[7]=="root":
			fields[7] = "ROOT";
	elif fields[7]=="punct":
			fields[7] = "p";
	elif fields[7]=="possessive":
			fields[7] = "adp";
	elif fields[7]=="abbrev":
			fields[7] = "appos";
	elif fields[7]=="number":
			fields[7] = "num";
	elif fields[7]=="npadvmod":
			fields[7] = "nmod";
	elif fields[7]=="prep":
			fields[7] = "adpmod";
	elif fields[7]=="pobj":
			fields[7] = "adpobj";
	elif fields[7]=="pcomp":
			fields[7] = "adpcomp";
	elif fields[7]=="purpcl":
			fields[7] = "advcl";
	elif fields[7]=="tmod":
		if fields[3]=="NOUN" or fields[3]=="NUM" or fields[3]=="PRON" or fields[3]=="X":
				fields[7] = "nmod";
		elif fields[3]=="ADV":
				fields[7] = "advmod";
		elif fields[3]=="ADJ":
				fields[7] = "amod";
		elif fields[3]=="ADP":
				fields[7] = "adpmod";
		elif fields[3]=="VERB":
				fields[7] = "advcl";
	elif fields[7]=="quantmod":
			fields[7] = "advmod";
	elif fields[7]=="complm":
			fields[7] = "mark";
	elif fields[7]=="predet":
			fields[7] = "det";
	elif fields[7]=="preconj":
			fields[7] = "cc";
	elif fields[7]=="nn":
			fields[7] = "compmod";
	elif fields[7]=="ps":
			fields[7] = "adp";
	return fields

if len(sys.argv)<3:
	print 'python standardize_english_conll.py pos_map_file conll_file output_file'
	sys.exit(0)


pos_map=read_pos_map(os.path.abspath(sys.argv[1]))


reader=open(os.path.abspath(sys.argv[2]),'r')
writer=open(os.path.abspath(sys.argv[3]),'w')
line=reader.readline()
while line:
	fields=line.strip().split('\t')
	if len(fields)<2:
		writer.write('\n')
	else:
		fields=normalizeWords(fields)
		fields=normalize_labels(fields)
		fields=normalize_tags(fields)
		if pos_map.has_key(fields[3]):
			fields[3]=pos_map[fields[3]]
			fields[4]='_'

		writer.write('\t'.join(fields).replace('\n','').replace('\r','')+'\n')

	line=reader.readline()

writer.flush()
writer.close()