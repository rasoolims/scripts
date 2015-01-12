import sys,codecs,os

orig_conll=codecs.open(os.path.abspath(sys.argv[1]),'r').read().split('\n\n')
fold_num=int(sys.argv[3])

ln=len(orig_conll)/fold_num


for i in range(1,fold_num+1):
	writer=codecs.open(os.path.abspath(sys.argv[2])+'_f_'+str(i),'w')
	for j in range((i-1)*ln,min(i*ln,len(orig_conll))):
		writer.write(orig_conll[j].strip()+'\n\n')
	writer.flush()
	writer.close()
