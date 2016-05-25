import os,sys,codecs
from collections import defaultdict

put_word_to_lemma = os.path.dirname(os.path.abspath(sys.argv[0]))+'/put_word_to_lemma.py'
input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'

for f in os.listdir(input_folder):
	command  = 'python '+put_word_to_lemma + ' '+input_folder+f +' '+ output_folder+f
	print command
	os.system(command)
