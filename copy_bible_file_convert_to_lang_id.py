import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<4:
	print 'input_folder langs_abr_file output_folder'

input_folder = os.path.abspath(sys.argv[1])+'/'
langs = {}
for line in open(os.path.abspath(sys.argv[2]),'r').read().strip().split('\n'):
 	l,c = line.split()
 	langs[l] = c
output_folder = os.path.abspath(sys.argv[3])+'/'


i = 0
for f in os.listdir(input_folder):
	l1,l2 = f.split('2')
	if l1 in langs and l2 in langs:
		command = 'cp '+input_folder+f+' '+output_folder+langs[l1]+'2'+langs[l2]
		print command
		os.system(command)