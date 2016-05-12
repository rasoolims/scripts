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
	for s in spl:
		freq_count[s]+=1
	count+=1
	if count%100000==0:
		sys.stdout.write(str(count)+'...')
	line1=reader1.readline()

print '\nrarify and write'

reader1=codecs.open(os.path.abspath(sys.argv[1]),'r')
line1=reader1.readline()
count = 0
while line1:
	spl=line1.strip().split(' ')
	
	output = list()
	for i in range(0,len(spl)):
		if freq_count[spl[i]]<5:
			output.append('_UNK_')
		else:
			output.append(spl[i])

	output.append('ROOT')
	writer1.write(' '.join(output)+'\n')
	count+=1
	if count%100000==0:
		sys.stdout.write(str(count)+'...')
	line1=reader1.readline()

print '\ndone!'