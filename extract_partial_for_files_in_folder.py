import os,sys,codecs
from collections import defaultdict

tree_extractor = os.path.dirname(os.path.abspath(sys.argv[0]))+'/extract_partial_trees_diff_sizes.py'

input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder_full = os.path.abspath(sys.argv[2])+'/'
output_folder_par7 = os.path.abspath(sys.argv[3])+'/'
output_folder_par5 = os.path.abspath(sys.argv[4])+'/'
output_folder_par1 = os.path.abspath(sys.argv[5])+'/'

i = 0
for f in os.listdir(input_folder):
	command  = 'python '+tree_extractor +' ' +input_folder+'  '+ output_folder_full+' '+output_folder_par7+' '+output_folder_par5+' '+output_folder_par1+' '+f
	i+= 1
	if i%5!=0 and i!=len(os.listdir(input_folder))-1:
		command+=' &'
	print command
	os.system(command)
print 'all done!==> delete the tmp files afterwards'


