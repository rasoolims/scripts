import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<4:
	print 'wikt_dict src_lang dst_lang output_folder'

input_folder = os.path.abspath(sys.argv[1])+'/'

for f in sorted(os.listdir(input_folder)):
	lines = codecs.open(input_folder+f,'r').read().strip().split('\n')

	words = set()
	num_words = 0

	for line in lines:
		spl = line.strip().split('\t')[0].split(' ')
		num_words+= len(spl)
		for s in spl:
			words.add(s)

	print f,len(lines),num_words,len(words)
