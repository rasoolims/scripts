import sys,os
script = os.path.dirname(os.path.abspath(sys.argv[0]))+'/reorder_tree_with_alignment_non_proj.py'
bible_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'

counter = 0
for f in os.listdir(bible_folder):
	l1, l2 = f.strip().split('_')
	folder = bible_folder+f+'/'

	src_conll = folder+'/corpus.tok.clean.'+l1+'.conll'
	dst_conll = folder+'/corpus.tok.clean.'+l2+'.conll'
	src_alignment = folder+l1+'2'+l2+'.grow.giza'
	dst_alignment = folder+l2+'2'+l1+'.grow.giza'
	l2_output = output_folder+ l1+'2'+l2+'.giza.reorder'
	l2_output_txt = output_folder+ l1+'2'+l2+'.tree'
	l1_output = output_folder+ l2+'2'+l1+'.giza.reorder'
	l1_output_txt = output_folder+ l2+'2'+l1+'.tree'


	src_command = ' '.join(['python -u',script, dst_conll, src_conll, src_alignment, l2_output, l2_output_txt, '&'])
	dst_command = ' '.join(['python -u',script, src_conll, dst_conll, dst_alignment, l1_output, l1_output_txt])
	
	counter += 2
	if counter<20:
		dst_command += ' &'
	else:
		counter = 0


	print src_command
	os.system(src_command)
	print dst_command
	os.system(dst_command)




