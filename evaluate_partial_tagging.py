import os,sys,math,operator,codecs,traceback
from collections import defaultdict

if len(sys.argv)<3:
	print 'python evaluate_partial_tagging.py [partial_file] [gold_file]'
	sys.exit(0)

partial_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
gold_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')

per_tag_cor=defaultdict(int)
tag_count=defaultdict(int)
tag_rec_count=defaultdict(int)
confusion=defaultdict(int)

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
					per_tag_cor[tags[i]]+=1
				else:
					tup=(tags[i],gold[i])
					confusion[tup]+=1
					#if tags[i]=='PRT' or gold[i]=='PRT':
						#print ws[i],tags[i],gold[i]
				tag_count[tags[i]]+=1
				tag_rec_count[gold[i]]+=1

	line=partial_reader.readline()

acc=100*float(c_count)/t_count
print round(acc,2)

for tag in per_tag_cor.keys():
	precision=100.0*float(per_tag_cor[tag])/tag_count[tag]
	recall=100.0*float(per_tag_cor[tag])/tag_rec_count[tag]
	fscore=2*precision*recall/(precision+recall)
	print tag,precision,recall,fscore,tag_rec_count[tag]

sorted_x = sorted(confusion.items(), key=operator.itemgetter(1),reverse=True)
for x in sorted_x:
	print x[0],x[1]