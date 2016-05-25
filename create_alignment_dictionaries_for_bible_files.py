import os,sys,codecs
from collections import defaultdict

dic_maker = os.path.dirname(os.path.abspath(sys.argv[0]))+'/create_dictionary_from_alignment.py'
input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'

i = 0
for flat_dir in os.listdir(input_folder):
	l1 = flat_dir[:flat_dir.rfind('_')]
	l2 = flat_dir[flat_dir.rfind('_')+1:]

	f = input_folder+flat_dir+'/'
	r1 = f + 'corpus.tok.clean.'+l1
	r2 = f + 'corpus.tok.clean.'+l2
	i1 = f + l1+'_'+l2+'.intersect'
	i2 = f + l2+'_'+l1+'.intersect'

	i+=1
	command  = 'python '+dic_maker + ' '+ r1 + ' '+r2 +' '+i1 + ' '+ output_folder + l1+'2'+l2+' &'
	print command
	os.system(command)

	i+=1
	command  = 'python '+dic_maker + ' '+ r2 + ' '+r1 +' '+i2+ ' '+ output_folder + l2+'2'+l1
	if i%10==0:
		command+= ' &'
	print command
	os.system(command)