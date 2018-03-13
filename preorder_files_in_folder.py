import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<6:
	print 'script_path embed_path model_path tree_path output_path'
	sys.exit(0)

script_path = os.path.abspath(sys.argv[1])
embed_path = os.path.abspath(sys.argv[2])
model_path = os.path.abspath(sys.argv[3])+'/'
tree_path = os.path.abspath(sys.argv[4])+'/'
output_path = os.path.abspath(sys.argv[5])+'/'

for f in os.listdir(model_path):
	command = 'nice python -u ' + script_path + ' --outdir ' + model_path+f+'/ --test ' + tree_path+f + ' --output ' + output_path + f + ' --extrn ' + embed_path
	print command
	os.system(command)
