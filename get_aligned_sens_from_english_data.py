import os,sys,codecs,random
from collections import defaultdict


sens=set(codecs.open(sys.argv[1],'r').read().strip().split('\n'))
reader1=codecs.open(sys.argv[2],'r')
reader2=codecs.open(sys.argv[3],'r')
writer1=codecs.open(sys.argv[4],'w')
writer2=codecs.open(sys.argv[5],'w')

output1=list()
output2=list()

line1=reader1.readline()
while line1:
	line2=reader2.readline().strip()
	line1=line1.strip()
	
	if line1 in sens:
		output1.append(line1)
		output2.append(line2)
		sens.remove(line1)

	line1=reader1.readline()

writer1.write('\n'.join(output1))
writer2.write('\n'.join(output2))
