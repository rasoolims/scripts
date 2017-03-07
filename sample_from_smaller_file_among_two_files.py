import os,sys,math,codecs,random

f1 = codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n')
f2 = codecs.open(os.path.abspath(sys.argv[2]),'r').read().strip().split('\n')
writer = codecs.open(os.path.abspath(sys.argv[3]),'w')

if len(f1)<len(f2):
	writer.write('\n'.join(f1))
	writer.write('\n')
	random.shuffle(f2)
	writer.write('\n'.join(f2[:len(f1)]))
else:
	writer.write('\n'.join(f2))
	writer.write('\n')
	random.shuffle(f1)
	writer.write('\n'.join(f1[:len(f2)]))

writer.close()