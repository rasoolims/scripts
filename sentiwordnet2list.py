import os,sys,codecs
from collections import defaultdict


lines = codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n')

senti_word_net = defaultdict(list)

for line in lines:
	if line.startswith('#'):
		continue
	spl = line.strip().split('\t')
	if len(spl)<2: continue
	pos_score = float(spl[2])
	neg_score = float(spl[3])
	entries = [word[:-2].lower() for word in spl[4].strip().split()]
	for entry in entries:
		senti_word_net[entry].append([pos_score,neg_score])

writer = codecs.open(os.path.abspath(sys.argv[2]),'w')
for word in senti_word_net.keys():
	scores = [0,0]
	for sc in senti_word_net[word]:
		scores[0]+= sc[0]
		scores[1]+= sc[1]
	for i in xrange(2): scores[i]/=len(senti_word_net[word])
	writer.write(word+'\t'+str(scores[0])+'\t'+str(scores[1])+'\n')
writer.close()