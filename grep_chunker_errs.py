import os,sys,codecs, operator

sentences = codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')

for sentence in sentences:
	lines = sentence.strip().split('\n')
	output = []
	has_err = False
	for line in lines:
		w,t,g,p = line.split()
		if g!=p:
			has_err = True
			output.append(line+' ***')
		else:
			output.append(line)
	if has_err:
		writer.write('\n'.join(output)+'\n\n')
writer.close()
