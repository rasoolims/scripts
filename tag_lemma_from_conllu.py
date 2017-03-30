import sys,codecs,os

orig_conll=codecs.open(os.path.abspath(sys.argv[1]),'r')
conllu_file=codecs.open(os.path.abspath(sys.argv[2]),'r')
writer=codecs.open(os.path.abspath(sys.argv[3]),'w')


line1=orig_conll.readline()
while line1:
	line2=conllu_file.readline()

	line1=line1.strip()
	line2=line2.strip()

	if line1:
		spl1=line1.split('\t')
		spl2=line2.split('\t')
		spl1[2]=spl2[2]
		writer.write('\t'.join(spl1)+'\n')
	else:
		writer.write('\n')

	line1=orig_conll.readline()

writer.flush()
writer.close()

