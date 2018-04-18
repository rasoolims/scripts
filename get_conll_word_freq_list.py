import os,sys,codecs,operator,math
from collections import defaultdict

sens=codecs.open(os.path.abspath(sys.argv[1]),'r').read().split('\n\n')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')
csv_writer=codecs.open(os.path.abspath(sys.argv[2])+'.csv','w')

freqs = defaultdict(int)

for sen in sens:
	lines=sen.strip().split('\n')
	words=list()
	for l in lines:
		if l.strip():
			freqs[l.strip().split('\t')[1].strip()]+=1

s = sorted(freqs.items(), key=operator.itemgetter(1),reverse=True)

frequent_words = set()

output,csv_output = [],['rank,logfreq']
last_w = ''
for c,w in enumerate(s):
	if len(w[0].strip())==0:
		continue
	output.append(str(c+1)+'\t'+w[0]+'\t'+str(math.log(w[1])))
	if (c+1)%5==1:
		csv_output.append(str(c+1)+','+str(math.log(w[1])))

writer.write('\n'.join(output))
writer.close()
csv_writer.write('\n'.join(csv_output))
csv_writer.close()