import os,sys,codecs
from collections import defaultdict

input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'


file_set = defaultdict(list)
for f in os.listdir(input_folder):
	l = f
	if '_' in l:
		l = f[:f.find('_')]
	file_set[l].append(input_folder+f)

for f in file_set.keys():
	print f
	command = "cat "+ ' '.join(file_set[f])+' > '+output_folder+f
	os.system(command)
	
