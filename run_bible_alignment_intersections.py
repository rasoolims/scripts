import os,sys,codecs
from collections import defaultdict

intersecter = os.path.dirname(os.path.abspath(sys.argv[0]))+'/get_alignment_intersection.py'
input_folder = os.path.abspath(sys.argv[1])+'/'

i = 0
for flat_dir in os.listdir(input_folder):
	l1 = flat_dir[:flat_dir.rfind('_')]
	l2 = flat_dir[flat_dir.rfind('_')+1:]

	f = input_folder+flat_dir+'/'
	al1 = f+l1+'_'+l2 + '.align.A3.final'
	al2 = f+l2+'_'+l1 + '.align.A3.final'

	i+=1
	command  = 'python '+intersecter + ' '+ al1 + ' '+al2 + ' '+ f + l1+'_'+l2+'.intersect &'
	print command
	os.system(command)

	i+=1
	command  = 'python '+intersecter + ' '+ al2 + ' '+al1 + ' '+ f + l2+'_'+l1+'.intersect'
	if i%10==0:
		command+= ' &'
	print command
	os.system(command)