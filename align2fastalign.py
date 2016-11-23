import os,sys,codecs

r1 = codecs.open(os.path.abspath(sys.argv[1]),'r')
r2 = codecs.open(os.path.abspath(sys.argv[2]),'r')
w = codecs.open(os.path.abspath(sys.argv[3]),'w')

l1 = r1.readline()
while l1:
	l2 = r2.readline()
	w.write(l1.strip()+' ||| '+l2.strip()+'\n')
	l1 = r1.readline()
w.close()