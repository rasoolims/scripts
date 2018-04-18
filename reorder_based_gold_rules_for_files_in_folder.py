import os,sys,codecs
from collections import defaultdict

script = os.path.dirname(os.path.abspath(sys.argv[0]))+'/reorder_based_on_gold_rules.py'
gold_treebank_folder = os.path.abspath(sys.argv[1])+'/'
orig_folder = os.path.abspath(sys.argv[2])+'/'
reorder_folder = os.path.abspath(sys.argv[3])+'/'

for lang in os.listdir(gold_treebank_folder):
	command = 'python  ' + script + ' ' + gold_treebank_folder+lang + ' ' + orig_folder + lang + ' '+ reorder_folder +lang + ' '+ lang
	print command
	os.system(command)