import os,sys,codecs
from collections import defaultdict

bible_tag_folder = os.path.abspath(sys.argv[1])+'/'
bible_order_folder = os.path.abspath(sys.argv[2])+'/'
order_folder = os.path.abspath(sys.argv[3])+'/'
output_folder = os.path.abspath(sys.argv[4])+'/'

for flat_dir in os.listdir(bible_tag_folder):
	orig_files = order_folder + flat_dir+'2*.tree.orig_words' 
	order_files = order_folder + flat_dir+'2*.giza.reorder' 
	command = 'cat ' + bible_tag_folder + flat_dir + ' ' + orig_files + '> ' + output_folder + flat_dir +'.tree &'
	#command = 'cat ' + orig_files + '> ' + output_folder + flat_dir +'.tree &'
	print command
	os.system(command)
	command = 'cat ' + bible_order_folder + flat_dir + ' ' + order_files + '> ' + output_folder + flat_dir +'.order &'
	#command = 'cat ' +  order_files + '> ' + output_folder + flat_dir +'.order &'
	print command
	os.system(command)
	