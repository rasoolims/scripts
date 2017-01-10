import os,sys,codecs
from collections import defaultdict

script = os.path.abspath(sys.argv[1])
input_folder = os.path.abspath(sys.argv[2])+'/'
output_folder = os.path.abspath(sys.argv[3])+'/'

for f in os.listdir(input_folder):
	command  = 'python '+script + ' '+input_folder+f +' '+ output_folder+f
	print command
	os.system(command)