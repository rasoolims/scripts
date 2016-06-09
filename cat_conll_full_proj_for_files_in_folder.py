import os,sys,codecs
from collections import defaultdict

input_folder1 = os.path.abspath(sys.argv[1])+'/'
input_folder2 = os.path.abspath(sys.argv[2])+'/'
output_folder = os.path.abspath(sys.argv[3])+'/'

for f in os.listdir(input_folder1):
	command  = 'cat '+ input_folder1+f+' '+ input_folder2+f + ' > '+output_folder+f
	print command
	os.system(command)
