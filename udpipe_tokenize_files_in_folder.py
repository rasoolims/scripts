import os,sys
from collections import defaultdict

if len(sys.argv)<6:
	print 'ud_pipe_script model_folder input_folder output_folder num_thread'
	sys.exit(0)


ud_pipe_script = os.path.abspath(sys.argv[1])
model_folder =  os.path.abspath(sys.argv[2])+'/'
input_folder =  os.path.abspath(sys.argv[3])+'/'
output_folder =  os.path.abspath(sys.argv[4])+'/'
num_thread = int(sys.argv[5])
to_skip = set()
if len(sys.argv)>6:
	to_skip = set(sys.argv[6].strip().split(','))


i  = 0
for f in sorted(os.listdir(input_folder)):
	l = f[f.rfind('.')+1:]
	model_file = model_folder+l
	if not l in to_skip:
		command = ud_pipe_script +' '+model_file+' --tokenizer=presegmented  --output horizontal '+ input_folder+f +' > '+output_folder+f
	else:
		command = 'cp '+ input_folder+f+' '+output_folder+f
	i+=1
	if i%num_thread !=0: command+='&'
	print command
	os.system(command)
