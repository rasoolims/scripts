import os,sys,codecs,math
from collections import defaultdict

freq_dict = defaultdict(int)

r1 = codecs.open(os.path.abspath(sys.argv[1]),'r')
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')
l1 = r1.readline()
max_freq = 0
while l1:
	ws = l1.strip().split()
	l1 = r1.readline()
	for w in ws:
		if w!='_RARE_':
			freq_dict[w]+=1

for w in freq_dict.keys():
	if freq_dict[w]>max_freq:
		max_freq = freq_dict[w]

freq_log = math.log(max_freq)

levels = [(i+1)*freq_log/5 for i in xrange(5)]

for w in freq_dict.keys():
	level = 0
	flog = math.log(freq_dict[w])
	for i in xrange(len(levels)):
		if flog<=levels[i]:
			level = i
			break

	writer.write(w+' '+str(level)+' '+str(freq_dict[w])+'\n')
writer.close()

