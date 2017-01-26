import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<6:
	print 'input_folder word2vec_path output_folder num_threads dim'
input_folder = os.path.abspath(sys.argv[1])+'/'
word2vec_path = os.path.abspath(sys.argv[2])
output_folder = os.path.abspath(sys.argv[3])+'/'
num_threads = int(sys.argv[4])
dim = int(sys.argv[5])


print os.listdir(input_folder)
commands = list()
for f in os.listdir(input_folder):
	print f
	command = 'cp '+input_folder+f + ' /tmp/'+f
	print command
	os.system(command)
	command = 'gunzip /tmp/'+f
	print command
	os.system(command)
	command = './'+word2vec_path+ ' -train /tmp/'+f + ' -output '+output_folder+f[:-3] + ' -size '+dim + ' -threads '+num_threads
	print command
	os.system(command)
	command = 'rm -f /tmp/'+f
	print command
	os.system(command)

print 'done!'