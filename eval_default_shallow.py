import os,sys,codecs, operator

sentences = codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')
correct = 0
all_ = 0
for sentence in sentences:
	lines = sentence.strip().split('\n')
	for line in lines:
		spl = line.split(' ')
		bio = spl[2]
		tag = spl[1]
		defBio = 'B-'+tag+'P'
		all_+=1
		if defBio==bio:
			correct+=1

print float(correct)/all_
