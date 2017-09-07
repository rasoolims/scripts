import os,sys
from collections import defaultdict

if len(sys.argv)<6:
	print 'ud_pipe_script train_folder dev_folder model_folder num_thread'
	sys.exit(0)


ud_pipe_script = os.path.abspath(sys.argv[1])
train_folder =  os.path.abspath(sys.argv[2])
dev_folder =  os.path.abspath(sys.argv[3])
model_folder =  os.path.abspath(sys.argv[4])
num_thread = int(sys.argv[5])


i  = 0
for f in sorted(os.listdir(train_folder)):
	train_file = train_folder+'/'+f
	dev_file = dev_folder+'/'+f
	model_file = model_folder+'/'+f
	command = ud_pipe_script +' --train '+model_file+' --heldout='+ dev_file+' '+ train_file +' --parser=none --tagger=none'
	i+=1
	if i%num_thread !=0: command+='&'
	print command
	os.system(command)
