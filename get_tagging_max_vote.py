import os,sys,codecs
from collections import defaultdict

sentences=defaultdict()

min_vote=int(sys.argv[-2])


for i in range(1,len(sys.argv)-2):
	print os.path.abspath(sys.argv[i])

	reader=codecs.open(os.path.abspath(sys.argv[i]),'r')
	line=reader.readline()
	
	count=0
	
	while line:
		count+=1
		
		spl=line.strip().split(' ')

		ws=list()
		tags=list()

		for s in spl:
			x=s.rfind('_')
			ws.append(s[:x])
			tags.append(s[x+1:])

		sen=' '.join(ws)

		if not sentences.has_key(sen):
			sentences[sen]=list()
			for i in range(0,len(ws)):
				sentences[sen].append(defaultdict(int))

		for i in range(0,len(tags)):
			if tags[i]!='***':
				sentences[sen][i][tags[i]]+=1

		if count%10000==0:
			sys.stdout.write(str(count)+'...')
		line=reader.readline()
	sys.stdout.write(str(count)+'\n')

writer=codecs.open(os.path.abspath(sys.argv[-1]),'w')

count=0
for sen in sentences:
	count+=1
	if count%10000==0:
		sys.stdout.write(str(count)+'...')
	words=sen.split(' ')
	output=list()

	d=sentences[sen]
	for i in range(0,len(d)):
		best_tag='***'
		mx=-1

		for t in d[i].keys():
			if d[i][t]>mx and d[i][t]>=min_vote:
				mx=d[i][t]
				best_tag=t

		output.append(words[i]+'_'+best_tag)

	writer.write(' '.join(output)+'\n')
sys.stdout.write('\n')

writer.flush()
writer.close()
