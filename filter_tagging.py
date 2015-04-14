import os,sys,math,operator,codecs,traceback
from collections import defaultdict

if len(sys.argv)<3:
	print 'python filter_trigrams.py [tag_file] [filtered_file]'
	sys.exit(0)

gold_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')

trigram_count=defaultdict(float)
bigram_count=defaultdict(int)

print 'reading gold tags...'
gold_tags=defaultdict()

line=gold_reader.readline()
while line:
	ws=list()
	tags=list()
	tags.append('*')
	tags.append('*')
	for l in line.strip().split(' '):
		r=l.rfind('_')
		tags.append(l[r+1:])
	tags.append('STOP')

	for i in range(2,len(tags)):
		bigram=tags[i-2]+' '+tags[i-1]
		bigram_count[bigram]+=1
		if not trigram_count.has_key(bigram):
			trigram_count[bigram]=defaultdict(int)
		trigram_count[bigram][tags[i]]+=1

	line=gold_reader.readline()

for bigram in trigram_count.keys():
	sorted_x = sorted(trigram_count[bigram].items(), key=operator.itemgetter(1),reverse=True)

	for s in sorted_x:
		trigram_count[bigram][s[1]]=100*float(s[1])/bigram_count[bigram]
		print bigram+' '+s[0],trigram_count[bigram][s[1]]
	print '*****************************************'


writer=codecs.open(os.path.abspath(sys.argv[2]),'w')

gold_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
line=gold_reader.readline()
while line:
	ws=list()

	tags=list()
	tags.append('*')
	tags.append('*')
	for l in line.strip().split(' '):
		r=l.rfind('_')
		tags.append(l[r+1:])
		ws.append(l[:r])
	tags.append('STOP')

	output=list()
	for i in range(2,len(tags)-1):
		bigram=tags[i-2]+' '+tags[i-1]
		bigram_count[bigram]+=1
		if trigram_count[bigram][tags[i]]>=10:
			output.append(ws[i-2]+'_'+tags[i])
		else:
			output.append(ws[i-2]+'_***')
	writer.write(' '.join(output)+'\n')

	line=gold_reader.readline()
writer.flush()
writer.close()