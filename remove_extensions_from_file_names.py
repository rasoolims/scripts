import os,sys
folder = os.path.abspath(sys.argv[1])+'/'
extension = sys.argv[2]
extension_len = len(extension)

for f in sorted(os.listdir(folder)):
	assert f.endswith(extension)
	l = folder+f[:-extension_len]
	print 'mv '+folder+f +' '+l
	os.system('mv '+folder+f +' '+l)