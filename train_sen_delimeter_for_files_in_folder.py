import os,sys,codecs
from collections import defaultdict

jar_file = os.path.abspath(sys.argv[1])
input_folder = os.path.abspath(sys.argv[2])+'/'
output_folder = os.path.abspath(sys.argv[3])+'/'


for f in os.listdir(input_folder):
	print f
	command = 'java -jar '+ jar_file+' SentenceDetectorTrainer -model '+ output_folder+f+' -lang '+ f +' -data '+ input_folder+f+' -encoding UTF-8'
	os.system(command)