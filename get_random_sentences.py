import os,sys,codecs,random
from collections import defaultdict

sens=codecs.open(sys.argv[1],'r').read().split('\n')

senlist=set()
count=0

while count<=50000:
	sen=sens[random.randint(0,len(sens))]
	if not sen in senlist:
		senlist.add(sen)
		count+=1


codecs.open(sys.argv[2],'w').write('\n'.join(senlist))