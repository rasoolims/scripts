import os,sys
from collections import defaultdict

folder = os.path.abspath(sys.argv[1])+'/'
odir = os.path.abspath(sys.argv[2])+'/'

files = defaultdict(list)

for f in sorted(os.listdir(folder)):
	l = f[:f.find('_')] if '_' in f else f
	files[l].append(folder+f)

for l in files.keys():
	command = 'cat '+' '.join(files[l])+' > '+odir+l
	print command
	os.system(command)