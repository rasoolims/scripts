import os,sys,codecs
from collections import defaultdict

retriever = os.path.dirname(os.path.abspath(sys.argv[0]))+'/retrieve_bible_parse_for_one_folder.py'
jar_file = os.path.abspath(sys.argv[1])
input_folder = os.path.abspath(sys.argv[2])+'/'
bible_folder = os.path.abspath(sys.argv[3])+'/'

lang_files = defaultdict(str)
for f in os.listdir(input_folder):
	lang_files[f] = input_folder+f

i = 0
for flat_dir in os.listdir(bible_folder):
	l1 = flat_dir[:flat_dir.rfind('_')]
	l2 = flat_dir[flat_dir.rfind('_')+1:]
	print l1,l2

	f = bible_folder+flat_dir+'/'
	command = 'python -u '+retriever + ' '+f +' '+lang_files[l1] + ' '+lang_files[l2] +' '+l1+ ' '+l2 +' '+jar_file
	i+=1
	if i%10!=0:
		command+=' &'
	print command
	os.system(command)

print 'done!'