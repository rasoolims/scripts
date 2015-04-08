import sys,os,codecs,operator
from collections import defaultdict

tags=dict()

if len(sys.argv)<4:
	print 'python extract_common_tag_dict.py [input_tagged_file] [small_wiki_file] [input_wiki_file]  [output_file]'
	sys.exit(0)

tag_dict=defaultdict()



print 'reading tags...'
line_count=0
reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
line=reader.readline()
while line:
	spl=line.strip().split(' ')
	for s in spl:
		i=s.rfind('_')
		w=s[:i].lower()
		t=s[i+1:]

		if not tag_dict.has_key(w):
			tag_dict[w]=defaultdict(int)

		tag_dict[w][t]+=1

	line=reader.readline()

small_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
line=small_reader.readline()
small_dict=defaultdict(set)
while line:
	spl=line.strip().split()
	word=spl[0].lower()
	tag=spl[1].lower()
	small_dict[word].add(tag)
	line=small_reader.readline()

reader2=codecs.open(os.path.abspath(sys.argv[3]),'r')
writer=codecs.open(os.path.abspath(sys.argv[4]),'w')
line=reader2.readline()
while line:
	spl=line.strip().split()
	word=spl[0].lower()
	tag=spl[1]
	if  (tag_dict.has_key(word) and tag in tag_dict[word]) or (small_dict.has_key(word) and tag in small_dict[word]):
		writer.write(line.strip()+'\n')

	line=reader2.readline()



writer.flush()
writer.close()