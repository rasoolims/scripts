import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<3:
	print 'input_file output_file'
	sys.exit(0)

input_file = os.path.abspath(sys.argv[1])
output_file = os.path.abspath(sys.argv[2])


writer = codecs.open(output_file,'w')
for line in codecs.open(input_file, 'r'):
	spl = line.strip().split()
	if len(spl)>2:
		if spl[-1]!='B-NP' and spl[-1]!='I-NP':
			spl[-1] = 'O'
		writer.write(' '.join(spl)+'\n')
	else:
		writer.write(line.strip()+'\n')
writer.close()