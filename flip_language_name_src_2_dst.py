import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<3:
	print 'input_folder output_folder'
	sys.exit(0)

input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'

for f in os.listdir(input_folder):
	l1,l2 = f.split('2')[0],f.split('2')[1]
	nf = l2+'2'+l1
	command = 'cp '+ input_folder+f+' '+output_folder+nf
	print command
	os.system(command)