import os,sys,codecs,random,gzip
from collections import defaultdict

if len(sys.argv)<4:
	print 'dic_folder wiki_folder output_path'
	sys.exit(0)


dic_folder = os.path.abspath(sys.argv[1])+'/'
wiki_folder = os.path.abspath(sys.argv[2])+'/'
output_path = os.path.abspath(sys.argv[3])
ratio = 0.3

dictionaries = dict()

print 'reading dictionaries...'
c = 0
for f in os.listdir(dic_folder):
	l1 = f[:f.rfind('2')]

	if not dictionaries.has_key(l1):
		dictionaries[l1]= defaultdict(list)

	rec = codecs.open(dic_folder+f,'r').read().strip().split('\n')
	dct = dictionaries[l1]
	for r in rec:
		spl = r.split('\t')
		dct[spl[0]].append(spl[1])
	c+=1
	if c%100==0:
		sys.stdout.write(str(c)+'...')

print '!'

writer = codecs.open(output_path,'w')

print 'code switching...'
c = 0
for f in os.listdir(wiki_folder):
	l = f
	if '.gz' in l:
		l = l[:-3]
	if not l in dictionaries:
		continue
	print f
	dct = dictionaries[l]
	reader = gzip.open(wiki_folder+f,'r')
	line = reader.readline()

	while line:
		spl = line.strip().split(' ')

		for j in range(0,len(spl)):
			if random.random()<ratio and dct.has_key(spl[j]):
				lst = dct[spl[j]]
				ind = random.randint(0,len(lst)-1)
				spl[j] = lst[ind]

		writer.write(' '.join(spl)+'\n')


		c+=1
		if c%100000==0:
			sys.stdout.write(str(c)+'...')

		line = reader.readline()
	writer.flush()
	print str(c)+'!'
writer.close()