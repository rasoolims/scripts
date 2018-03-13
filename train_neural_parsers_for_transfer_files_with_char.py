import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<6:
	print 'parser_path treebank_folder_path embedding_path output_folder languages'
	sys.exit(0)
parser_path = os.path.abspath(sys.argv[1])+'/'
treebank_path = os.path.abspath(sys.argv[2])+'/'
embedding_path = os.path.abspath(sys.argv[3])
output_folder = os.path.abspath(sys.argv[4])+'/'
t = int(sys.argv[5])
languages = sys.argv[6].strip().split(',')

for i, language in enumerate(languages):
	print 'SCRIPT: training for language', language
	if not os.path.isdir(output_folder+language): os.mkdir(output_folder+language)
	command = 'python -u ' + parser_path+ '/src/parser.py  --outdir '+ output_folder+language+' --train '\
	 + treebank_path+ language + ' --extrn ' + embedding_path + ' --t '+str(t)+ ' > '+ output_folder+language+'/nohups.out '
	print 'SCRIPT:',command
	os.system(command)
	print 'SCRIPT: done with language', language
print 'SCRIPT: finished!'