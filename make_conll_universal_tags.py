import os,sys,math,codecs

if len(sys.argv)<4:
	print 'python make_conll_universal_tags.py [mapping_file] [input_conll] [output_conll]'
	sys.exit(0)

mapping_dict=dict()
tr=open(os.path.abspath(sys.argv[1]),'r').read().split('\n')
for t in tr:
	t=t.strip()
	if t:
		mapping_dict[t.split('\t')[0]]=t.split('\t')[1]
		mapping_dict[t.split('\t')[0].lower()]=t.split('\t')[1]

reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
writer=codecs.open(os.path.abspath(sys.argv[3]),'w')
line=reader.readline()
while line:
	line=line.strip()
	spl=line.split()
	if len(spl)<6:
		writer.write('\n')
	else:
		if mapping_dict.has_key(spl[3]):
			spl[3]=mapping_dict[spl[3]]
		elif  mapping_dict.has_key(spl[4]):
			spl[3]=mapping_dict[spl[4]]
		#elif mapping_dict.has_key(spl[3][0:2]):
			#spl[3]=mapping_dict[spl[3][0:2]]
		#elif mapping_dict.has_key(spl[3][0:2]):
			#spl[3]=mapping_dict[spl[3][0:1]]
		#elif spl[3].startswith('f'):
			#spl[3]='.'
		writer.write('\t'.join(spl)+'\n')

	line=reader.readline()

writer.flush()
writer.close()
