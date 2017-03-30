import os,sys
from collections import defaultdict

if len(sys.argv)<7:
	print 'python_script  train_folder dev_folder model_folder num_iter num_thread'
	sys.exit(0)


python_script = os.path.abspath(sys.argv[1])
train_folder =  os.path.abspath(sys.argv[2])+'/'
dev_folder =  os.path.abspath(sys.argv[3])+'/'
model_folder =  os.path.abspath(sys.argv[4])+'/'
num_iter = int(sys.argv[5])
num_thread = int(sys.argv[6])

command = 'export MKL_NUM_THREADS=1'
os.system(command)

i  = 0
for f in sorted(os.listdir(train_folder)):
	train_file = train_folder+f
	dev_file = dev_folder+f
	model_file = model_folder+f
	if not os.path.isdir(model_file): os.mkdir(model_file)
	log_file = model_file+'/log.txt'

	command = 'nice python -u '+ python_script +' --train '+ train_file +' --dev '+ dev_file +' --outdir '+ model_file+ ' --save_best --epochs '+ str(num_iter) +' > ' + log_file
	i+=1
	if i%num_thread!=0:
		command+='&'
	print command
	os.system(command)
print 'done!'