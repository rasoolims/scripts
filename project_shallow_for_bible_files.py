import os,sys,codecs
from collections import defaultdict

projector = os.path.dirname(os.path.abspath(sys.argv[0]))+'/project_shallow_trees.py'
input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'

i = 0
for flat_dir in os.listdir(input_folder):
	l1 = flat_dir[:flat_dir.rfind('_')]
	l2 = flat_dir[flat_dir.rfind('_')+1:]

	f = input_folder+flat_dir+'/'
	r1 = f + 'corpus.tok.clean.'+l1+'.conll.shallow'
	r2 = f + 'corpus.tok.clean.'+l2+'.conll.tag'
	r3 = f + 'corpus.tok.clean.'+l1+'.conll.tag'
	r4 = f + 'corpus.tok.clean.'+l2+'.conll.shallow'
	i1 = f + l1+'_'+l2+'.intersect'
	i2 = f + l2+'_'+l1+'.intersect'

	i+=1
	command  = 'python '+projector + ' '+ r1 + ' '+r2 +' '+i1 + ' '+ output_folder + l1+'2'+l2+' false &'
	print command
	os.system(command)

	i+=1
	command  = 'python '+projector + ' '+ r4 + ' '+r3 +' '+i2+ ' '+ output_folder + l2+'2'+l1 + ' false '
	if i%10==0:
		command+= ' &'
	print command
	os.system(command)