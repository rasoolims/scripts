import os,sys,codecs

if len(sys.argv)<3:
	print 'python get_parse_for_raw_file.py [reference mst] [raw file] [output file]'
	sys.exit(0)

src_mst_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')

src_trees=dict()
line=src_mst_reader.readline()
line_count=0
while line:
	line=line.strip()
	if line:
		output=list()
		line_count+=1
		words=line.split('\t')
		output.append(line)
		output.append(src_mst_reader.readline().strip())
		output.append(src_mst_reader.readline().strip())
		output.append(src_mst_reader.readline().strip())
		output.append('')

		sentence=' '.join(words)


		src_trees[sentence]=output
		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')
	line=src_mst_reader.readline()

sys.stdout.write('\n')

raw_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
writer=codecs.open(os.path.abspath(sys.argv[3]),'w')

line=raw_reader.readline()
line_count=0
while line:
	line_count+=1
	writer.write('\n'.join(src_trees[line.strip()]))
	if line_count%100000==0:
		sys.stdout.write(str(line_count)+'...')
	line=raw_reader.readline()
writer.flush()
writer.close()

