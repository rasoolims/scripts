import sys,codecs,random,os

f = codecs.open(os.path.abspath(sys.argv[1]),'r')
wr =  codecs.open(os.path.abspath(sys.argv[2]),'w')

for r in f:
	spl = r.strip().split('\t')
	words = spl[0].split()
	output = [w+'|||'+str(random.randint(1,5)) for w in words]
	wr.write(' '.join(output)+'\t'+spl[1]+'\n')
wr.close()	