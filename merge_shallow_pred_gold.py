import os,sys,codecs, operator

sentences = codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')
gold_sentences = codecs.open(os.path.abspath(sys.argv[2]),'r').read().strip().split('\n\n')
writer = codecs.open(os.path.abspath(sys.argv[3]),'w')

for i in xrange(len(sentences)):
	sentence = sentences[i]
	gold_sentence = gold_sentences[i]
	lines = sentence.strip().split('\n')
	g_lines = gold_sentence.strip().split('\n')
	output = []
	for i in xrange(len(lines)):
		w,t,p = lines[i].split()
		w,t,g = g_lines[i].split()
		line = w+' '+t+' '+' '+g+' '+p
		output.append(line)
	
	writer.write('\n'.join(output)+'\n\n')
writer.close()
