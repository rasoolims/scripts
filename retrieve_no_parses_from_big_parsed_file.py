import os,sys,codecs

if len(sys.argv)<4:
	print 'python retrieve_no_parses_from_big_parsed_file.py [big_parse_file] [input_tagged_file] [output_parse_file]'
	sys.exit(0)

# creating parse dictionaries from big parse files
print 'reading sentences (may take a while)....'
parses=codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')


print 'creating dictionaries'
parse_dict=dict()

for parse in parses:
	flds=parse.strip().split('\n')
	sen=list()
	for f in flds:
		w=f.split('\t')[1]
		if w:
			sen.append(w)
	parse_dict[' '.join(sen)]=parse.strip()

parses=None

print 'reading tagged file and writing to the output parse file'
reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
writer=codecs.open(os.path.abspath(sys.argv[3]),'w')
line=reader.readline()
count=0
while line:
	sen=list()
	for f in line.strip().split(' '):
		w=f[:f.rfind('_')]
		if w:
			sen.append(w)

	if not parse_dict.has_key(' '.join(sen)):
		writer.write(line.strip()+'\n')
	count+=1
	if count%100000==0:
		sys.stdout.write(str(count)+'...')
	line=reader.readline()

sys.stdout.write('done!\n')

writer.flush()
writer.close()
