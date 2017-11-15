import sys,codecs,os

orig_conll=codecs.open(os.path.abspath(sys.argv[1]),'r')
tag_conll=codecs.open(os.path.abspath(sys.argv[2]),'r')
writer=codecs.open(os.path.abspath(sys.argv[3]),'w')


line1=orig_conll.readline()
while line1:
	line2=tag_conll.readline()

	line1=line1.strip()
	line2=line2.strip()

	if line1:
		spl1=line1.split('\t')
		spl2=line2.split('\t')
		spl1[1]=spl2[1]
		spl1[2]=spl2[2]
		spl1[3]=spl2[3]
		spl1[4]=spl2[4]
		writer.write('\t'.join(spl1)+'\n')

	else:
		writer.write('\n')

	line1=orig_conll.readline()

writer.flush()
writer.close()

