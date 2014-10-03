import os,sys,codecs

sens=codecs.open(os.path.abspath(sys.argv[1]),'r').read().split('\n\n')
tagged_sens=codecs.open(os.path.abspath(sys.argv[2]),'r').read().split('\n')
writer=codecs.open(os.path.abspath(sys.argv[3]),'w')

cntr=0
for sen in sens:
	lines=sen.strip().split('\n')
	words=list()

	w_cntr=0
	tagged_words=tagged_sens[cntr].strip().split(' ')
	for l in lines:
		split_line=l.split('\t')
		if len(split_line)>1:
			split_line[3]=tagged_words[w_cntr].split('_')[1]
			split_line[4]=tagged_words[w_cntr].split('_')[1]
			w_cntr+=1
		words.append('\t'.join(split_line))

	writer.write('\n'.join(words)+'\n\n')
	cntr+=1

writer.flush()
writer.close()