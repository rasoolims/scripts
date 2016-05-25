import os,sys,codecs
from collections import defaultdict

conll2raw = os.path.dirname(os.path.abspath(sys.argv[0]))+'/conll2raw_detok.py'
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
	command = "cat "+ ' '.join(file_set[f])+' > '+ '/tmp/'+f+'.tmp'
	os.system(command)
	command  = 'python '+conll2raw + ' '+'/tmp/'+f+'.tmp'+ '  '+output_folder+f + ' true'
	os.system(command)
	os.system('rm -f '+'/tmp/'+f+'.tmp')

