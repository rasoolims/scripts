import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<6:
	print 'input_folder python_path model_path embed_path output_folder'
	sys.exit(0)
input_folder = os.path.abspath(sys.argv[1])+'/'
python_path = os.path.abspath(sys.argv[2])
model_path = os.path.abspath(sys.argv[3])+'/'
embed_path = os.path.abspath(sys.argv[4])
output_folder = os.path.abspath(sys.argv[5])+'/'


print os.listdir(input_folder)
commands = list()
for f in os.listdir(input_folder):
	print f
	l = f
	if '_' in f:
		l = f[:f.find('_')]
	if '.' in l:
		l = l[l.rfind('.')+1:]
	if not os.path.isdir(model_path+l ):
		print 'skipped', f
		continue
	command = 'nice python -u ' + python_path+ ' --predict --test '+ input_folder+f +' --model '+model_path+l + '/model --params '+ model_path+l+'/params.pickle --output ' + output_folder+f + ' --extrn '+embed_path
	print command
	os.system(command)
