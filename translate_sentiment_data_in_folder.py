import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<5:
	print 'tranlate_script input_folder dict_folder output_folder'
	sys.exit(0)

translate_script = os.path.abspath(sys.argv[1])
input_folder = os.path.abspath(sys.argv[2])+'/'
dict_folder = os.path.abspath(sys.argv[3])+'/'
output_folder = os.path.abspath(sys.argv[4])+'/'

input_files = set(os.listdir(input_folder))
for f in os.listdir(dict_folder):
	l1,l2 = f.split('2')[0],f.split('2')[1]
	if l1 in input_files:
		command = 'python -u  '+ translate_script+' '+dict_folder+f+' '+input_folder+l1+' '+output_folder+f
		print command
		os.system(command)