import sys,codecs,os
from collections import defaultdict

word_count = defaultdict(int)

rare_count = int(sys.argv[3])
print 'reading'
cnt = 0
reader = codecs.open(os.path.abspath(sys.argv[1]),'r')
line = reader.readline()
while line:
	line = line.strip()
	cnt +=1
	if cnt%100000==0:
		sys.stdout.write(str(cnt)+'...')
	if line:
		spl = line.split()
		for s in spl:
			word_count[s]+=1
	line = reader.readline()

sys.stdout.write(str(cnt)+'\n')
cnt = 0

print 'writing...'
reader = codecs.open(os.path.abspath(sys.argv[1]),'r')
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')
line = reader.readline()
while line:
	line = line.strip()
	cnt +=1
	if cnt%100000==0:
		sys.stdout.write(str(cnt)+'...')
	if line:
		spl = line.split()
		for i in range(0,len(spl)):
			if word_count[spl[i]]<rare_count:
				spl[i] = '_RARE_'
		writer.write(' '.join(spl)+'\n')
	line = reader.readline()

writer.close()
sys.stdout.write(str(cnt)+'\n')


