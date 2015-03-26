import os,sys,codecs
from random import randint

sens=codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')
needed=int(sys.argv[2])
writer=codecs.open(os.path.abspath(sys.argv[3]),'w')
generated=set()

count=0

while count<needed:
	g=randint(0,len(sens))
	if not g in generated:
		generated.add(g)
		count+=1
		writer.write(sens[g].strip()+'\n\n')
		if count%1000==0:
			sys.stdout.write(str(count)+'...')

writer.flush()
writer.close()
sys.stdout.write('\n')
