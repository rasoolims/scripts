import sys,os
script = os.path.dirname(os.path.abspath(sys.argv[0]))+'/reorder_with_alignment_with_density_filter.py'
bible_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'
final_folder = os.path.abspath(sys.argv[3])+'/'
source_langs = set(['cop', 'ar', 'he', 'id', 'eu', 'ja', 'fi', 'da', 'de', 'en', 'nl', 'no', 'sv', 'hi', 'fa', 'el', 'es', 'fr', 'it', 'pt', 'ro', 'bg', 'cs', 'hr', 'pl', 'ru', 'sk', 'sl'])
proportion = str(float(sys.argv[4]))

counter = 0
dst_langs = set()
last_command = None
for f in os.listdir(bible_folder):
	l1, l2 = f.strip().split('_')
	folder = bible_folder+f+'/'
	dst_langs.add(l1)
	dst_langs.add(l2)

	l1_conll = folder+'/corpus.tok.clean.'+l1+'.conll'
	l2_conll = folder+'/corpus.tok.clean.'+l2+'.conll'
	l1_2_union = folder+'/'+l1+'_'+l2+'.union'
	l2_1_union = folder+'/'+l2+'_'+l1+'.union'

	if l1 in source_langs:
		first_command = ' '.join(['python -u',script, l1_conll, l2_conll, l2_1_union, proportion, output_folder+ l1+'2'+l2, '&'])
		counter += 1
		print first_command
		os.system(first_command)
		if last_command is None:
			last_command = first_command
	if l2 in source_langs:
		second_command = ' '.join(['python -u',script, l2_conll, l1_conll, l1_2_union, proportion, output_folder+ l2+'2'+l1])
		counter += 1
		if counter<20:
			second_command += ' &'
		else:
			counter = 0

		print second_command
		os.system(second_command)

		if last_command is None:
			last_command = second_command

last_command = last_command.replace('&', '')
os.system(last_command)

for dst_lang in dst_langs:
	command = 'cat ' + output_folder + '*2'+dst_lang + ' > ' + final_folder + dst_lang
	print command
	os.system(command)



