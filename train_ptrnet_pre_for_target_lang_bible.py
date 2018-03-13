import os,sys,codecs
from collections import defaultdict

script_path = os.path.abspath(sys.argv[1])
bible_folder = os.path.abspath(sys.argv[2])+'/'
model_folder = os.path.abspath(sys.argv[3])+'/'
target_lang = sys.argv[4]
extrn = os.path.abspath(sys.argv[5])+'/'
source_langs = set(sys.argv[6].strip().split(','))

if not os.path.isdir(model_folder):
	print 'mkdir '+model_folder
	os.system('mkdir '+model_folder)

i = 0
for flat_dir in os.listdir(bible_folder):
	l1, l2 = flat_dir.split('_')
	if l1 != target_lang and l2 != target_lang:
		continue
	if l2==target_lang:
		l2, l1 = l1, l2
	source_lang = l2
	if not source_lang in source_langs:
		continue
	print flat_dir
	m = model_folder+'/'+l2+'2'+l1
	if not os.path.isdir(m):
		print 'mkdir '+m
		os.system('mkdir '+m)
	min_freq = 2 if target_lang == 'en' else 1

	command = 'nice python -u '+ script_path + ' --train '+bible_folder+flat_dir+'/corpus.tok.clean.'+source_lang+'.conll.tag --train_t '+bible_folder+flat_dir+'/'+l1+'2'+l2+'.giza.reorder --outdir ' + m+ ' --batch 1000 --extrn ' + extrn + source_lang + '.gz --min_freq ' +str(min_freq) + ' --dropout 0 --epoch 10 > ' + m + '/log_2.txt'
	print command
	os.system(command)
print 'done with language', target_lang
