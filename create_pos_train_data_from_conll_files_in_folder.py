import os,sys,codecs
from collections import defaultdict

conll_to_pos_path = os.path.dirname(os.path.abspath(sys.argv[0]))+'/conll2tag.py'
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
	tmp_conll_path = '/tmp/'+f+'.conll.tmp'
	command = 'nice cat '+' '.join(lang_files[f])+' > ' + tmp_conll_path
	os.system(command)
	command = 'python '+conll_to_pos_path+' '+tmp_conll_path + ' '+output_folder+f
	os.system(command)
	command = 'rm -f '+tmp_conll_path
	os.system(command)


