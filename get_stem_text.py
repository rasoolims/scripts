import os,sys,codecs

if len(sys.argv)<3:
	print 'python get_stem_text.py [input_text] [stem_file] [output_text]'
	sys.exit(0)

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
stem_lines=codecs.open(os.path.abspath(sys.argv[2]),'r').read().strip().split('\n')
writer=codecs.open(os.path.abspath(sys.argv[3]),'w')

stems=dict()
for st in stem_lines:
	spl=st.split('\t')
	stems[spl[0]]=spl[1]

count=0
line=reader.readline()
while line:
	spl=line.strip().split(' ')
	count+=1
	if count%100000==0:
		sys.stdout.write(str(count)+'...')
	output=list()
	for s in spl:
		s=s.lower()
		if s:
			if stems.has_key(s):
				output.append(stems[s])
			else:
				output.append(s)
	writer.write(' '.join(output)+'\n')
	line=reader.readline()

sys.stdout.write('\n')
writer.flush()
writer.close()

