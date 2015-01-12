import sys,os,codecs,operator

trees=dict()

if len(sys.argv)<2:
	print 'python extract_partial_trees.py [input_mst] [output_mst]'
	sys.exit(0)

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')

print 'reading trees...'
line_count=0

line=reader.readline()
while line:
	line=line.strip()
	if line:
		line_count+=1
		words=line
		tags=reader.readline().strip()
		labels=reader.readline().strip()
		hds=reader.readline().strip()
		
		spl=hds.split('\t')

		is_full=True
		for s in spl:
			if s=='-1':
				is_full=False
		if not is_full:
			writer.write(words+'\n')
			writer.write(tags+'\n')
			writer.write(labels+'\n')
			writer.write(hds+'\n\n')

		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')
	line=reader.readline()
sys.stdout.write('done!\n')
writer.flush()
writer.close()