import os,sys,codecs,math
from collections import defaultdict

print 'reading sentences'

sens=codecs.open(os.path.abspath(sys.argv[1]),'r').read().split('\n')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')


bigram_count = defaultdict(int)
trigram_count = defaultdict(int)

print 'reading grams'
for sen in sens:
	sen = '<START> <START> '+sen +' <END>'
	words = sen.strip().split(' ')
	for i in range(2, len(words)):
		trigram = words[i-2]+' '+words[i-1]+' '+words[i]
		bigram = words[i-2]+' '+words[i-1]
		bigram_count[bigram]+=1
		trigram_count[trigram]+=1

print 'writing probs'
for trigram in trigram_count.keys():
	bigram = trigram.split(' ')[0]+' '+ trigram.split(' ')[1]
	prob = math.log(float(trigram_count[trigram])/bigram_count[bigram])
	writer.write(trigram+'\t'+str(prob)+'\n')
writer.close()


