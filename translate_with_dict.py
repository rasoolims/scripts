import os,sys,codecs

trans = {line.strip().split()[0]:line.strip().split()[1] for line in codecs.open(os.path.abspath(sys.argv[1]),'r')}
writer =codecs.open(os.path.abspath(sys.argv[3]),'w')

for line in codecs.open(os.path.abspath(sys.argv[2]),'r'):
	try:
		sen,label = line.strip().split('\t')
		output = []
		for word in sen.strip().split():
			if word in trans:
				output.append(word+'|||'+trans[word])
			else:
				output.append(word)
		writer.write(' '.join(output)+'\t'+label+'\n')
	except:
		print line
		#sys.exit(1)
writer.close()