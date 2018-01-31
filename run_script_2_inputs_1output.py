import os,sys,codecs
from collections import defaultdict

script = os.path.abspath(sys.argv[1])
input_folder1 = os.path.abspath(sys.argv[2])+'/'
input_folder2 = os.path.abspath(sys.argv[3])+'/'
output_folder = os.path.abspath(sys.argv[4])+'/'

for f in os.listdir(input_folder1):
	command  = 'python '+script + ' '+input_folder1+f + ' '+input_folder2+f +' '+ output_folder+f
	print command
	os.system(command)