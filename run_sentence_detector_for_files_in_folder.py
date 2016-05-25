import os,sys,codecs
from collections import defaultdict

jar_file = os.path.abspath(sys.argv[1])
model_folder = os.path.abspath(sys.argv[2])+'/'
input_folder = os.path.abspath(sys.argv[3])+'/'
output_folder = os.path.abspath(sys.argv[4])+'/'


for f in os.listdir(input_folder):
	l = f
	if f.endswith('.txt'):
		l = f[:-4]
	print l
	model = model_folder  + l
	command = 'java -jar '+ jar_file+' SentenceDetector '+ model+' < '+input_folder+f+' > '+output_folder+l
	os.system(command)