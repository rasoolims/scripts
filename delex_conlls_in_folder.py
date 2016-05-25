import os,sys,codecs
from collections import defaultdict

conll_delexer = os.path.dirname(os.path.abspath(sys.argv[0]))+'/delex_conll.py'
input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'

for f in os.listdir(input_folder):
	command  = 'python '+conll_delexer + ' '+input_folder+f + ' _ '+output_folder+f
	print command
	os.system(command)
