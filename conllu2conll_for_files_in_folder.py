import os,sys,codecs
from collections import defaultdict

script = os.path.dirname(os.path.abspath(sys.argv[0]))+'/conllu2conll.py'
input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'

for f in os.listdir(input_folder):
	l = f[:f.find('_')] if '_' in f else f
	command  = 'python '+script + ' '+input_folder+f +' '+l+' '+ output_folder+f
	print command
	os.system(command)