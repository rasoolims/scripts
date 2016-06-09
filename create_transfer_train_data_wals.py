import os,sys,codecs
from collections import defaultdict

lang_info_file = os.path.abspath(sys.argv[1])
info = codecs.open(lang_info_file,'r').read().strip().split('\n')

lang_info = defaultdict(list)
for inf in info:
	spl = inf.split('\t')
	lang_info[spl[1]] = spl[5:]
print lang_info.keys()

def lang_sim(l1,l2):
	sim = 0
	for i in range(0,len(lang_info[l1])):
		#print l1,l2,i
		if lang_info[l1][i]==lang_info[l2][i]:
			sim+=1
	return sim

input_folder = os.path.abspath(sys.argv[2])+'/'
output_folder = os.path.abspath(sys.argv[3])+'/'
min_count = int(sys.argv[4])

lang_files = defaultdict(list)
for f in sorted(os.listdir(input_folder)):
	l = f
	if '_' in l:
		l = f[:f.find('_')]
	lang_files[l].append(input_folder+f)

for f in sorted(lang_files.keys()):
	print f
	train_files = list()
	lang_set = set()
	for f2 in lang_files.keys():
		if f==f2 or lang_sim(f,f2)<min_count:
			continue
		lang_set.add(f2)
		for fl in lang_files[f2]:
			train_files.append(fl)
	command = 'nice cat '+' '.join(train_files)+' > ' + output_folder+f
	print f,'->',' '.join(lang_set)
	os.system(command)
