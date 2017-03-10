import os,sys,codecs

if len(sys.argv)<2:
	print 'input_folder'

input_folder = os.path.abspath(sys.argv[1])+'/'

for f in os.listdir(input_folder):
	l1,l2 = f.split('2')
	nf = input_folder+l2+'.'+l1
	command = 'mv '+input_folder+f+' '+nf
	print command
	os.system(command)