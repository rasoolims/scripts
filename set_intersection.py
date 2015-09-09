import os,sys,codecs,random
from collections import defaultdict

sens=list()

for i in range(1,len(sys.argv)-1):
	print sys.argv[i]
	sens.append(set())
	sens[i-1]=set(codecs.open(sys.argv[i],'r').read().split('\n'))


u=set.intersection(*sens)

codecs.open(sys.argv[len(sys.argv)-1],'w').write('\n'.join(u))