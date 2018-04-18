import os,sys,codecs
from collections import defaultdict

script = os.path.dirname(os.path.abspath(sys.argv[0]))+'/mix_orig_reorder_trees_based_on_scores.py'
gold_treebank_folder = os.path.abspath(sys.argv[1])+'/'
orig_folder = os.path.abspath(sys.argv[2])+'/'
reorder_folder = os.path.abspath(sys.argv[3])+'/'
output_folder = os.path.abspath(sys.argv[4])+'/'

for lang in os.listdir(gold_treebank_folder):
	command = 'python  ' + script + ' ' + gold_treebank_folder+lang + ' ' + orig_folder + lang + ' '+ reorder_folder +lang + ' '+ output_folder + lang
	print command
	os.system(command)