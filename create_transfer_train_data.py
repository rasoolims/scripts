import os,sys,codecs
from collections import defaultdict

input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'

lang_files = defaultdict(list)
for f in os.listdir(input_folder):
	l = f
	if '_' in l:
		l = f[:f.find('_')]
	lang_files[l].append(input_folder+f)

for f in lang_files:
	print f
	train_files = list()
	for f2 in lang_files:
		if f==f2:
			continue
		for fl in lang_files[f2]:
			train_files.append(fl)
	command = 'nice cat '+' '.join(train_files)+' > ' + output_folder+f
	os.system(command)
