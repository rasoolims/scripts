import os,sys,codecs
from collections import defaultdict

input_folder1 = os.path.abspath(sys.argv[1])+'/'
input_folder2 = os.path.abspath(sys.argv[2])+'/'
input_folder3 = os.path.abspath(sys.argv[3])+'/'
output_folder = os.path.abspath(sys.argv[4])+'/'



counter = 0
print 'reading to set...'
for f in os.listdir(input_folder1):
	f1 = input_folder1 + f
	f2 = input_folder2 + f
	f3 = input_folder3 + f
	command = 'cat ' + f1+' '+f2+' '+f3 +' > ' + output_folder+f
	print command
	os.system(command)
print 'done!'

