import sys,os,codecs,operator
from collections import defaultdict

tags=dict()

if len(sys.argv)<4:
	print 'python extract_tag_dict.py [input_tagged_file] [threshold] [output_file]'
	sys.exit(0)

tag_dict=defaultdict()

threshold=float(sys.argv[2])


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

print 'writing tags...'
writer=codecs.open(os.path.abspath(sys.argv[3]),'w')
for w in tag_dict.keys():
	all_count=0
	for t in tag_dict[w].keys():
		all_count+=tag_dict[w][t]

	for t in tag_dict[w].keys():
		prob=float(tag_dict[w][t])/all_count
		if prob>=threshold:
			writer.write(w+'\t'+t+'\n')

writer.flush()
writer.close()