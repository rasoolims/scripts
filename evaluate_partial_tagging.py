import os,sys,math,operator,codecs,traceback
from collections import defaultdict

if len(sys.argv)<3:
	print 'python evaluate_partial_tagging.py [partial_file] [gold_file]'
	sys.exit(0)

partial_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
gold_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')

print 'reading gold tags...'
gold_tags=defaultdict()

line=gold_reader.readline()
while line:
	ws=list()
	tags=list()
	for l in line.strip().split(' '):
		r=l.rfind('_')
		ws.append(l[:r])
		tags.append(l[r+1:])

	gold_tags[' '.join(ws)]=tags

	line=gold_reader.readline()

t_count=0
c_count=0

print 'reading partial tags...'
line=partial_reader.readline()
while line:
	ws=list()
	tags=list()
	for l in line.strip().split(' '):
		r=l.rfind('_')
		ws.append(l[:r])
		tags.append(l[r+1:])
	words=' '.join(ws)
	if gold_tags.has_key(words):
		gold=gold_tags[words]

		for i in range(0,len(tags)):
			if tags[i]!='***':
				t_count+=1
				if tags[i]==gold[i]:
					c_count+=1

	line=partial_reader.readline()

acc=100*float(c_count)/t_count
print round(acc,2)