import os,sys,codecs
from optparse import OptionParser

lines = codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n')
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')
for_decode = True if len(sys.argv)>3 and sys.argv[3]=='decode' else False
lower = True if len(sys.argv)>4 and sys.argv[4]=='lower' else False

for line in lines:
	output = []
	for f in line.strip().split():
		word = f[:f.rfind('_')]
		tag = f[f.rfind('_')+1:]
		if lower: word=word.lower()
		if for_decode:
			output.append(word+'|||'+tag)
		else:
			output.append(word+'|||'+word+'|||'+tag)
	writer.write(' '.join(output)+'\n')
writer.close()