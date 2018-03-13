import os,sys,codecs
from collections import defaultdict

bible_folder = os.path.abspath(sys.argv[1])+'/'
target_lang = sys.argv[2]
output_path = os.path.abspath(sys.argv[3])
is_lex = True if len(sys.argv)>4 and sys.argv[4]=='lex' else False
print is_lex

tag_outputs, reorder_outputs = [], []
i = 0
for flat_dir in os.listdir(bible_folder):
	l1, l2 = flat_dir.split('_')
	if l1 != target_lang and l2 != target_lang:
		continue
	if l2 == target_lang:
		l2, l1 = l1, l2
	source_lang = l2

	extension = '.lex.conll.tag' if is_lex else '.conll.tag'
	tag_contents = codecs.open(bible_folder+flat_dir+'/corpus.tok.clean.'+source_lang+extension, 'r').read().strip().split('\n')
	tag_outputs += tag_contents
	reorder_contents = codecs.open(bible_folder+flat_dir+'/'+l1+'2'+l2+'.giza.reorder', 'r').read().strip().split('\n')
	reorder_outputs += reorder_contents

print len(tag_outputs), len(reorder_outputs)

codecs.open(output_path+'.tag', 'w').write('\n'.join(tag_outputs))
codecs.open(output_path+'.reorder', 'w').write('\n'.join(reorder_outputs))
