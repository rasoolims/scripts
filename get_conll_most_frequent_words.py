import os,sys,codecs,operator
from collections import defaultdict

sens=codecs.open(os.path.abspath(sys.argv[1]),'r').read().split('\n\n')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')
freqs = defaultdict(int)

for sen in sens:
	lines=sen.strip().split('\n')
	words=list()
	for l in lines:
		if l.strip():
			freqs[l.strip().split('\t')[1].strip()]+=1



s = sorted(freqs.items(), key=operator.itemgetter(1),reverse=True)

frequent_words = set()

c = 0
last_f = 10000
last_w = ''
for w in s:
	if len(w[0].strip())==0:
		continue
	if c>2000 and w[1]!=last_f:
		print last_w, last_f
		break
	else:
		last_f = w[1]

	frequent_words.add(w[0])
	if not w[0].isdigit():
		c+=1
		last_w = w[0]

writer.write('\n'.join(frequent_words))
writer.flush()
writer.close()