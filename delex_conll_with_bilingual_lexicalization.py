import os,sys,codecs

reader1=codecs.open(os.path.abspath(sys.argv[1]),'r')

dic_entries = codecs.open(os.path.abspath(sys.argv[2]),'r').read().strip().split('\n')

word_dict = dict()

for ent in dic_entries:
	spl = ent.strip().split()
	word_dict[spl[0].lower()] = spl[1].lower()


writer1=codecs.open(os.path.abspath(sys.argv[3]),'w')

line1=reader1.readline()

while line1:
	spl=line1.strip().split('\t')
	if len(spl)>2:
		if word_dict.has_key(spl[1].lower()):
			spl[1] = word_dict[spl[1].lower()]
		else:
			spl[1]='_'
		spl[2]='_'
		writer1.write('\t'.join(spl)+'\n')
	else:
		writer1.write(line1)

	line1=reader1.readline()
writer1.close()