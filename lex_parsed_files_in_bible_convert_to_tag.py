import os,sys,codecs,random
from collections import defaultdict


if len(sys.argv)<3:
	print 'dic_folder bible_folder'
	sys.exit(0)

conll2tag = os.path.dirname(os.path.abspath(sys.argv[0]))+'/conll2tag.py'
lexer = os.path.dirname(os.path.abspath(sys.argv[0]))+'/lex_parser_sub_code.py'

dic_folder = os.path.abspath(sys.argv[1])+'/'
input_folder = os.path.abspath(sys.argv[2])+'/'
use_in_word = True
ratio = 0.3

dictionaries = defaultdict()


print 'code switching...'
c = 0
for f in os.listdir(input_folder):
	l1,l2 = f.strip().split('_')
	print f

	file1 = input_folder+f+'/'+'corpus.tok.clean.'+l1+'.conll'
	file1_out = input_folder+f+'/'+'corpus.tok.clean.'+l1+'.lex.conll'
	file1_tag_out = input_folder+f+'/'+'corpus.tok.clean.'+l1+'.lex.conll.tag'
	intersect_file1 = input_folder+f+'/'+ l1 + '_'+l2+'.intersect'
	dict_path1 = dic_folder + l1 + '2' + l2

	file2 = input_folder+f+'/'+'corpus.tok.clean.'+l2+'.conll'
	file2_out = input_folder+f+'/'+'corpus.tok.clean.'+l2+'.lex.conll'
	file2_tag_out = input_folder+f+'/'+'corpus.tok.clean.'+l2+'.lex.conll.tag'
	intersect_file2 = input_folder+f+'/'+ l2 + '_'+l1+'.intersect'
	dict_path2 = dic_folder + l2 + '2' + l1
	
	arguments = [[file1, file1_out, file1_tag_out, intersect_file1, file2, dict_path1], [file2, file2_out, file2_tag_out, intersect_file2, file1, dict_path2]]
	

	for arg_ in arguments:
		c+= 1
		command = ['python -u', lexer] + arg_ 
		if c % 20 != 0:
			command += ['&']
		command = ' '.join(command)
		print command
		os.system(command)