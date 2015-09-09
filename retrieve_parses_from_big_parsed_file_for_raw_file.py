import os,sys,codecs

if len(sys.argv)<4:
	print 'python retrieve_parses_from_big_parsed_file_for_raw_file.py [big_parse_file] [input_raw_file] [output_parse_file]'
	sys.exit(0)

# creating parse dictionaries from big parse files
print 'reading sentences (may take a while)....'
parses=codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')


print 'creating dictionaries'
parse_dict=dict()

for parse in parses:
	flds=parse.strip().split('\n')
	sen=flds[0].split('\t')
	parse_dict[' '.join(sen).strip()]=parse.strip()

parses=None

print len(parse_dict)

print 'reading raw file and writing to the output parse file'
reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
writer=codecs.open(os.path.abspath(sys.argv[3]),'w')
line=reader.readline()
count=0
while line:
	try:
		parse=parse_dict[line.strip()]
		writer.write(parse+'\n\n')
		count+=1
		if count%100000==0:
			sys.stdout.write(str(count)+'...')
	except:
		parse=parse_dict[line.strip().replace('\'s','\' s')]
		writer.write(parse+'\n\n')
		count+=1
		if count%100000==0:
			sys.stdout.write(str(count)+'...')
	line=reader.readline()

sys.stdout.write('done!\n')

writer.flush()
writer.close()
