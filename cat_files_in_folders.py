import os,sys

i1_dir = os.path.abspath(sys.argv[1])+'/'
i2_dir = os.path.abspath(sys.argv[2])+'/'
o_dir =  os.path.abspath(sys.argv[3])+'/'

for f in os.listdir(i1_dir):
	command = 'cat '+i1_dir+f+' '+i2_dir+f + '> '+ o_dir+f
	print command
	os.system(command)
