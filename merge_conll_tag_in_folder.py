import os,sys,codecs
from collections import defaultdict

merge_conll_tag = os.path.dirname(os.path.abspath(sys.argv[0]))+'/merge_conll_tag.py'
input_conll_folder = os.path.abspath(sys.argv[1])+'/'
input_tag_folder = os.path.abspath(sys.argv[2])+'/'
output_folder = os.path.abspath(sys.argv[3])+'/'

for f in os.listdir(input_tag_folder):
	command  = 'python '+merge_conll_tag + ' '+input_conll_folder+f + ' '+input_tag_folder+f +' ' +output_folder+f
	print command
	os.system(command)

print os.listdir(input_conll_folder)