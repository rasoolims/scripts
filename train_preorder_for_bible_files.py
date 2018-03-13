import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<6:
	print 'script_path train_path embed_path langs model_path'
	sys.exit(0)

script_path = os.path.abspath(sys.argv[1])
train_path = os.path.abspath(sys.argv[2])+'/'
embed_path = os.path.abspath(sys.argv[3])
langs = set(sys.argv[4].strip().split(','))
model_path = os.path.abspath(sys.argv[5])+'/'

for f in langs:
	if not os.path.isdir(model_path+f):
		os.mkdir(model_path+f)
	command = 'python -u ' + script_path + ' --train ' + train_path+f+'.tree --train_t ' + train_path +f+'.order --outdir ' + model_path + f + ' --batch 1000 --epoch 10 --min_freq 1 --dropout 0 --dev_percent 1 --extrn ' + embed_path + ' > ' + model_path+f+'/log.out ' 

	print command
	os.system(command)
	print 'done with', f