import os,sys,codecs

reader1=codecs.open(os.path.abspath(sys.argv[1]),'r')
reader2=codecs.open(os.path.abspath(sys.argv[2]),'r')


train_words = set()
test_words = set()

line1=reader1.readline()
while line1:
	spl=line1.strip().split('\t')
	if len(spl)>2:
		train_words.add(spl[1])

	line1=reader1.readline()

line1=reader2.readline()
while line1:
	spl=line1.strip().split('\t')
	if len(spl)>2:
		test_words.add(spl[1])

	line1=reader2.readline()

print len(train_words)
print len(test_words)

intersect = train_words & test_words

diff =len(test_words)-len(intersect)
print diff

prp = float(diff)/len(test_words)
print prp