import os,sys,codecs
from collections import defaultdict

convertor = os.path.dirname(os.path.abspath(sys.argv[0]))+'/put_word_to_lemma.py'
input_folder = os.path.abspath(sys.argv[1])+'/'
jar_file = os.path.abspath(sys.argv[2])
output_folder = os.path.abspath(sys.argv[3])+'/'

lang_files = defaultdict(list)
for f in os.listdir(input_folder):
	l1 = f[f.rfind('2')+1:]
	lang_files[l1].append(input_folder+f)


i = 0 
for l in lang_files.keys():
	command  = 'java -jar  '+jar_file +' '+' '.join(lang_files[l])+' '+output_folder+l
	i+=1
	if i%5 != 0:
		command+=' &'
	print command
	os.system(command)
