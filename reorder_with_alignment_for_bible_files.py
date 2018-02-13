import sys,os
script = os.path.dirname(os.path.abspath(sys.argv[0]))+'/reorder_with_alignment.py'
bible_folder = os.path.abspath(sys.argv[1])+'/'

for f in os.listdir(bible_folder):
	l1, l2 = f.strip().split('_')
	folder = bible_folder+f+'/'

	src_tags = folder+'/corpus.tok.clean.'+l1
	dst_tags = folder+'/corpus.tok.clean.'+l2
	src_alignment = folder+l1+'2'+l2+'.grow.fastalign'
	dst_alignment = folder+l2+'2'+l1+'.grow.fastalign'
	l2_output = folder+ l1+'2'+l2+'.reorder'
	l2_output_txt = folder+ l1+'2'+l2+'.reorder.txt'
	l1_output = folder+ l2+'2'+l1+'.reorder'
	l1_output_txt = folder+ l2+'2'+l1+'.reorder.txt'

	src_command = ' '.join(['python -u',script, dst_tags, src_tags, src_alignment, l2_output, l2_output_txt, '&'])
	dst_command = ' '.join(['python -u',script, src_tags, dst_tags, dst_alignment, l1_output, l1_output_txt])

	print src_command
	os.system(src_command)
	print dst_command
	os.system(dst_command)




