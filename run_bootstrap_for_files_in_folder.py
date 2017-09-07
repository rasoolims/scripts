import os,sys,codecs

jar_file = os.path.abspath(sys.argv[1])
gold_folder = os.path.abspath(sys.argv[2])+'/'
t1_folder = os.path.abspath(sys.argv[3])+'/'
neutral_folder = os.path.abspath(sys.argv[4])+'/'

for f in os.listdir(t1_folder):
	lf = f
	if 'en2' in f:
		f = f[3:]
	print f

	command = 'java -jar '+jar_file + ' '+gold_folder+f+ ' '+ t1_folder+lf + ' '+ neutral_folder+f + ' 24'
	print command
	os.system(command)
