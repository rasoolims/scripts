import os,sys,codecs
from collections import defaultdict

converter = os.path.dirname(os.path.abspath(sys.argv[0]))+'/dep_universal1_2_maximal.py'
input_folder = os.path.abspath(sys.argv[1])+'/'

i = 1
for flat_dir in os.listdir(input_folder):
	for f in os.listdir(input_folder+flat_dir):
		if f.endswith('.conll'):
			file_address = input_folder+flat_dir+'/'+f
			output_file = input_folder+flat_dir+'/'+f + '.shallow'
			command = 'nice python -u ' + converter+' ' + file_address + ' ' + output_file
			i += 1
			if i%10 != 0:
				command += ' &'
			print command
			os.system(command)
