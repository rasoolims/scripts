import os,sys,codecs

input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'

for f in os.listdir(input_folder):
	if os.path.exists(input_folder+f+'/test.out'):
		if not os.path.exists(output_folder+f):
			command = 'cp '+input_folder+f+'/test.out '+output_folder+f
			print command
			os.system(command)