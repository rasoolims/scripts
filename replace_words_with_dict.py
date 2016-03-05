import os,sys,codecs,random
from collections import defaultdict

if len(sys.argv)< 4:
	print 'dict_file input_file output_file'
	sys.exit(0)

dictionaries = defaultdict(list)
dic_reader = codecs.open(os.path.abspath(sys.argv[1]),'r')
line = dic_reader.readline()
while line:
	spl = line.strip().split()
	if len(spl)>1:
		dictionaries[spl[1]].append(spl[0])
	line = dic_reader.readline()


reader = codecs.open(os.path.abspath(sys.argv[2]),'r')
writer = codecs.open(os.path.abspath(sys.argv[3]),'w')
line = reader.readline()
cnt = 0
rc = 0
while line:
	spl = line.strip().split()
	k = 0
	already = set()
	for i in range(0,len(spl)):
		r = random.randint(0,len(spl)-1)

		if not r in already and dictionaries.has_key(spl[r]):
			cands = dictionaries[spl[r]]
			ri = random.randint(0, len(cands)-1)
			spl[r] = cands[ri]
			rc += 1
			k+=1
		already.add(r)
		if k==3:
			break
	cnt += 1
	if cnt%10000 ==0:
		sys.stdout.write(str(cnt)+'...')
	writer.write(' '.join(spl)+'\n')
	line = reader.readline()
writer.close()
sys.stdout.write(str(cnt)+'\n')
print rc