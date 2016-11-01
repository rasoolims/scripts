import os,sys,codecs
from collections import defaultdict

tree_extractor = os.path.dirname(os.path.abspath(sys.argv[0]))+'/extract_trees_conll.py'

input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder_full = os.path.abspath(sys.argv[2])+'/'
output_folder_par7 = os.path.abspath(sys.argv[3])+'/'
output_folder_par5 = os.path.abspath(sys.argv[4])+'/'
output_folder_par1 = os.path.abspath(sys.argv[5])+'/'

i = 0
for f in os.listdir(input_folder):
	command = 'python -u '+ tree_extractor +' 100000 1.1 '+ input_folder+f +' '+output_folder_full+f + ' 50 &'
	print command
	os.system(command)

	command = 'python -u '+ tree_extractor +' 7 0.8 '+ input_folder+f +' '+output_folder_par7+f + ' 50 partial &'
	print command
	os.system(command)

	command = 'python -u '+ tree_extractor +' 5 0.8 '+ input_folder+f +' '+output_folder_par5+f + ' 50 partial &'
	print command
	os.system(command)

	command = 'python -u '+ tree_extractor +' 1 0.8 '+ input_folder+f +' '+output_folder_par1+f + ' 50 partial '
	print command
	os.system(command)

print 'all done!'


