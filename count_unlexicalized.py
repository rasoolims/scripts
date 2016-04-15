import os,sys,codecs

reader1=codecs.open(os.path.abspath(sys.argv[1]),'r')

types = set()
tokens = 0
all_types = set()
all_tokens = 0

line1=reader1.readline()
while line1:
	spl=line1.strip().split('\t')

	if len(spl)>4:
		if spl[1]=='_':
			tokens+=1
			types.add(spl[2])
		all_tokens+=1
		all_types.add(spl[2])
	
	line1=reader1.readline()

print 'tokens',tokens
print 'all_tokens',all_tokens
tp = 100.0*tokens/all_tokens
print '%',"{0:.2f}".format(tp)

print 'all_types',len(types)
print 'all_types',len(all_types)
tp = 100.0*len(types)/len(all_types)
print '%',"{0:.2f}".format(tp)
