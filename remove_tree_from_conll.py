# coding: utf8

import os,sys,codecs
from collections import defaultdict

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')
line=reader.readline()
while line:
	line=line.strip()
	spl=line.split('\t')

	if len(spl)>7:
		spl[6], spl[7] = '-1', '_'
		writer.write('\t'.join(spl)+'\n')
	else:
		writer.write(line+'\n')
	line=reader.readline()

writer.flush()
writer.close()