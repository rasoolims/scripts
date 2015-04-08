import os,sys,codecs
from collections import defaultdict

sens_dict=defaultdict()

sens=codecs.open(os.path.abspath(sys.argv[1]),'r').read().split('\n')

for sen in sens:
	words=list()
	for s in sen.strip().split(' '):
		words.append(s.split('_')[0])
	sens_dict[' '.join(words)]=sen.strip()


writer=codecs.open(os.path.abspath(sys.argv[2]),'w')

for s in sens_dict.keys():
	writer.write(sens_dict[s]+'\n')

writer.flush()
writer.close()