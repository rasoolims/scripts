import os,sys,codecs
from collections import defaultdict 

reader1=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer1=codecs.open(os.path.abspath(sys.argv[2]),'w')


line1=reader1.readline()
count = 0

freq_count = defaultdict(int)

print 'creating freq_count'
while line1:
	spl=line1.strip().split(' ')
	spl.append('ROOT')
	writer1.write(' '.join(spl)+'\n')
	count+=1
	if count%100000==0:
		sys.stdout.write(str(count)+'...')
	line1=reader1.readline()

print '\ndone!'