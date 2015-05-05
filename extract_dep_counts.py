import os,sys,codecs,operator
from collections import defaultdict

sens=codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')


pairs=defaultdict(int)
tag_dict=set()

for sen in sens:
	heads=list()
	tags=list()

	fs=sen.strip().split('\n')

	for f in fs:
		ts=f.split()
		heads.append(int(ts[6]))
		tags.append(ts[3])

	for i in range(0,len(heads)):
		h=heads[i]
		dep_tag=tags[i]
		tag_dict.add(dep_tag)
		head_tag='ROOT'
		tag_dict.add(head_tag)
		if h>0:
			head_tag=tags[h-1]

		pair=head_tag+'->'+dep_tag
		pairs[pair]+=1



#for ps in  sorted(pairs.items(), key=operator.itemgetter(1),reverse=True):
	#print ps[0],ps[1]

for t1 in tag_dict:
	for t2 in tag_dict:
		p=t1+'->'+t2

		count=pairs[p]

		reward=0
		if count>20000:
			reward=4
		elif count>10000:
			reward=3
		elif count>5000:
			reward=2
		elif count>1000:
			reward=1
		elif count>100:
			reward=-1
		elif count>0:
			reward=-2
		elif count==0:
			reward=-3

		print t1,t2,reward
