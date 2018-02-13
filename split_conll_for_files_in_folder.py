import os,sys

split_conll = os.path.dirname(os.path.abspath(sys.argv[0]))+'/split_conll.py'
data = os.path.abspath(sys.argv[1])+'/'
proportion = float(sys.argv[2])
train_folder  = os.path.abspath(sys.argv[3])+'/'
test_folder = os.path.abspath(sys.argv[4])+'/'

for f in os.listdir(data):	
	command = ' '.join(['python', split_conll, data+ f, str(proportion), train_folder+ f, test_folder+ f])
	print command
	os.system(command)