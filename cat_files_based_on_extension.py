import os,sys
from collections import defaultdict

if len(sys.argv)<3:
	print 'input_folder output_folder'
	sys.exit(0)


input_folder =  os.path.abspath(sys.argv[1])+'/'
output_folder =  os.path.abspath(sys.argv[2])+'/'

exts = set()
for f in sorted(os.listdir(input_folder)):
	extension = f[f.rfind('.')+1:]
	exts.add(extension)

for ex in exts:
	command = 'cat '+ input_folder+'*.'+ex+' |sort  | uniq > '+output_folder+ex +' &'
	print command
	os.system(command)