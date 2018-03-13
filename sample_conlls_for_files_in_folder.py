import os,sys

sampler = os.path.dirname(os.path.abspath(sys.argv[0]))+'/sample_conlls.py'
folder = os.path.abspath(sys.argv[1])+'/'
o_folder = os.path.abspath(sys.argv[2])+'/'
max_num = int(sys.argv[3])

for f in sorted(os.listdir(folder)):
	command = 'python ' + sampler + ' '+folder+f +' '+o_folder+f + ' '+str(max_num) + '&'
	print command
	os.system(command)
