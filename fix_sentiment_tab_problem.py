import os,sys,codecs
from collections import defaultdict

skipped= 0
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')
for sentence in codecs.open(os.path.abspath(sys.argv[1]),'r'):
	sentence = sentence.strip().replace('\t',' ').replace('  ',' ').replace('  ',' ')
	spl = sentence.strip().split()
	if len(spl)>=2:
		writer.write(' '.join(spl[:-1]).lower()+'\t'+spl[-1]+'\n')
	else:
		skipped += 1
writer.close()
print 'skipped',skipped