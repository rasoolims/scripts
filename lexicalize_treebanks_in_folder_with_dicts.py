import os,sys,codecs,random
from collections import defaultdict

if len(sys.argv)<4:
	print 'dic_folder input_folder output_folder'
	sys.exit(0)


dic_folder = os.path.abspath(sys.argv[1])+'/'
input_folder = os.path.abspath(sys.argv[2])+'/'
output_folder = os.path.abspath(sys.argv[3])+'/'
use_in_word = False
if len(sys.argv)>4 and sys.argv[4]=='true':
	use_in_word = True
ratio = 0.3

dictionaries = defaultdict()

print 'reading dictionaries...'
c = 0
for f in os.listdir(dic_folder):
	dictionaries[f]= defaultdict()

	rec = codecs.open(dic_folder+f,'r').read().strip().split('\n')
	for r in rec:
		spl = r.split('\t')
		dictionaries[f][spl[0]] = spl[1]
	c+=1
	if c%100==0:
		sys.stdout.write(str(c)+'...')
print '!'


print 'code switching...'
c = 0
for f in os.listdir(input_folder):
	print f
	writer = codecs.open(output_folder+f,'w')
	reader = codecs.open(input_folder+f,'r')
	line = reader.readline()
	while line:
		spl = line.strip().split('\t')
		if len(spl)>6:
			l_id = spl[5]
			lp = l_id+'2'+f
			spl[1] = spl[1].lower()
			if dictionaries[lp].has_key(spl[1]):
				if not use_in_word:
					spl[2] = spl[1]
					spl[1] = dictionaries[lp][spl[1]]
				else:
					spl[1] = dictionaries[lp][spl[1]]
					spl[2] = spl[1]
			elif spl[3]=='PUNCT' or spl[3]=='.':
				spl[2] = spl[1]
			else:
				if not use_in_word:
					spl[2] = spl[1]
					spl[1] = spl[1]
				else:
					spl[2] = spl[1]

		writer.write('\t'.join(spl)+'\n')
		line = reader.readline()

