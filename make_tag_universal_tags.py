import os,sys,math,codecs

if len(sys.argv)<4:
	print 'python make_tag_universal_tags.py [mapping_file] [input_tagged] [output_tagged]'
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
	if line.strip():


		spl=line.replace('  ',' ').replace('  ',' ').strip().split(' ')

		output=list()
		for s in spl:
			x=s.rfind('_')
			word=s[:x]
			tag=s[x+1:]

			tag=mapping_dict[tag]
			output.append(word+'_'+tag)

	writer.write(' '.join(output)+'\n')

	line=reader.readline()

writer.close()