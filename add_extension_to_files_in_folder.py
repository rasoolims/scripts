import os,sys
folder = os.path.abspath(sys.argv[1])+'/'
extension = sys.argv[2]

for f in sorted(os.listdir(folder)):
	os.system('mv '+folder+f +' '+folder+f+extension)