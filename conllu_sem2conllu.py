import os,sys,codecs


writer = codecs.open(os.path.abspath(sys.argv[2]),'w')
for line in codecs.open(os.path.abspath(sys.argv[1]),'r'):
	spl = line.strip().split('\t')
	writer.write('\t'.join(spl[:10])+'\n')
writer.close()