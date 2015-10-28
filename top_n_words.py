import os,sys,codecs,operator
from collections import defaultdict


count_dict = defaultdict(int)
lines=codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n')
mx = int(sys.argv[2])
writer = codecs.open(os.path.abspath(sys.argv[3]),'w')

for line in lines:
	spl = line.split(' ')
	for s in spl:
		count_dict[s]+=1


sorted_count_dict = sorted(count_dict.items(), key=operator.itemgetter(1),reverse=True)

cnt = 0
for s in sorted_count_dict:
	if len(s[0].strip())<=2:
		continue
	writer.write(s[0]+'\n')
	cnt+=1
	if cnt> mx:
		break

writer.close()