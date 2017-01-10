import os,sys,codecs,random

data = codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')
proportion = float(sys.argv[2])
w1 = codecs.open(os.path.abspath(sys.argv[3]),'w')
w2 = codecs.open(os.path.abspath(sys.argv[4]),'w')

for d in data:
	if random.uniform(0,1)<proportion:
		w1.write(d+'\n\n')
	else:
		w2.write(d+'\n\n')
w1.close()
w2.close()