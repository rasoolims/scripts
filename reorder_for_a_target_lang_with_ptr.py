import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<7:
	print 'script_path tree_file model_folder target_lang extrn output_folder'
	sys.exit(0)

extractor = os.path.dirname(os.path.abspath(sys.argv[0]))+'/extract_trees_based_on_lang_id.py'
script_path = os.path.abspath(sys.argv[1])
tree_file = os.path.abspath(sys.argv[2])
model_folder = os.path.abspath(sys.argv[3])+'/'
target_lang = sys.argv[4]
extrn = os.path.abspath(sys.argv[5])+'/'
output_folder = os.path.abspath(sys.argv[6])+'/'

if not os.path.isdir(output_folder):
	print 'mkdir '+output_folder
	os.system('mkdir '+output_folder)

command = 'nice python -u '+ extractor + ' ' + tree_file + ' '+ target_lang + ' ' + output_folder + target_lang+'2'+target_lang+'.reorder'
print command
os.system(command)

i = 0
for flat_dir in os.listdir(model_folder):
	l1, l2 = flat_dir.split('2')
	if l2 != target_lang:
		continue
	
	print flat_dir
	m = model_folder+'/'+flat_dir
	
	command = 'nice python -u '+ extractor + ' ' + tree_file + ' '+ l1 + ' ' + output_folder + flat_dir
	print command
	os.system(command)

	command = 'nice python -u '+ script_path + ' --test '+ output_folder + flat_dir +' --outdir ' + m+ ' --batch 1000 --extrn ' + extrn + l1 + '.gz --output '+ output_folder + flat_dir+'.reorder'
	i += 1
	if i%2 == 1:
		command += ' &'
	print command
	os.system(command)
command = 'cat '+output_folder+'/*2'+target_lang+'.reorder > '+ output_folder+'/'+target_lang
print command
os.system(command)
print 'done with language', target_lang