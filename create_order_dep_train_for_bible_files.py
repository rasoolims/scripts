import os,sys,codecs
from collections import defaultdict

bible_tag_folder = os.path.abspath(sys.argv[1])+'/'
order_folder = os.path.abspath(sys.argv[2])+'/'
output_folder = os.path.abspath(sys.argv[3])+'/'

for flat_dir in os.listdir(bible_tag_folder):
	orig_files = order_folder + flat_dir+'2*.tree.complex' 
	order_files = order_folder + flat_dir+'2*.giza.reorder' 
	output_order = order_folder + flat_dir+'2*.giza.reorder.complex' 
	command = 'cat ' + orig_files + '> ' + output_folder + flat_dir +'.tree &'
	print command
	os.system(command)
	command = 'cat ' +  order_files + '> ' + output_folder + flat_dir +'.order &'
	print command
	os.system(command)
	command = 'cat ' +  output_order + '> ' + output_folder + flat_dir +'.order.complex &'
	print command
	os.system(command)