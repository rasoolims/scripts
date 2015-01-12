import os,sys,codecs
reader1=codecs.open(os.path.abspath(sys.argv[1]),'r')
reader2=codecs.open(os.path.abspath(sys.argv[2]),'r')
labeled=True if sys.argv[3]=='true' else False

line1=reader1.readline()
sen1=list()
sen2=list()
cor_tree=True
sen_num=1
while line1:
	line2=reader2.readline()

	spl1=line1.strip().split('\t')
	spl2=line2.strip().split('\t')

	if len(spl1)>6:
		cor=False
		if spl1[6]=='-1' or spl2[6]=='-1' or spl1[6]==spl2[6]:
			if labeled:
				if spl1[6]=='-1' or spl2[6]=='-1' or spl1[7]==spl2[7]:
					cor=True
			else:
				cor=True

		sen1.append(line1.strip())
		sen2.append(line2.strip())
		if not cor:
			cor_tree=False
	else:
		if not cor_tree:
			print '\n'.join(sen1)+'\n'
			print '\n'.join(sen2)
			print sen_num
			sys.exit(0)
		sen_num+=1
		sen1=list()
		sen2=list()

	line1=reader1.readline()