import os,sys,codecs, re
from collections import defaultdict

numberRegex = re.compile("[0-9]+|[0-9]+\\.[0-9]+|[0-9]+[0-9,]+");


def normalize(word):
    return 'NUM' if numberRegex.match(word) else word.lower()


print 'word count'
word_count = defaultdict(int)
for i, sen in enumerate(codecs.open(os.path.abspath(sys.argv[1]),'r')):
	words = [normalize(word) for word in sen.strip().split()]
	for w in words:
		word_count[w]+=1
	if i%1000==0:
		sys.stdout.write(str(i)+'...'+'\r')

print '\rnormalization'
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')
for i, sen in enumerate(codecs.open(os.path.abspath(sys.argv[1]),'r')):
	words = [normalize(word) for word in sen.strip().split()] 
	words = [word if word_count[word]>1 else '_UNK_' for word in words]
	writer.write(' '.join(words)+'\n')
	if i%1000==0:
		sys.stdout.write(str(i)+'...'+'\r')
writer.close()
print '\r'
