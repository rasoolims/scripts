import os,sys,codecs
from collections import defaultdict

dense_pipeline = os.path.dirname(os.path.abspath(sys.argv[0]))+'/dense_pipeline_no_eval.py'

jar_file = os.path.abspath(sys.argv[1])
cluster_folder = os.path.abspath(sys.argv[2])+'/'
folder_full = os.path.abspath(sys.argv[3])+'/'
folder_par7 = os.path.abspath(sys.argv[4])+'/'
folder_par5 = os.path.abspath(sys.argv[5])+'/'
folder_par1 = os.path.abspath(sys.argv[6])+'/'
output_folder = os.path.abspath(sys.argv[7])+'/'
min_cnt = int(sys.argv[8])
max_cnt = int(sys.argv[9])

i = 0
for f in os.listdir(folder_full):
	if i>=min_cnt and i<=max_cnt:
		arguments = list()
		arguments.append(jar_file)
		arguments.append(folder_full+f)
		arguments.append(folder_par7+f)
		arguments.append(folder_par5+f)
		arguments.append(folder_par1+f)
		arguments.append("/tmp/"+f)
		arguments.append('3 3 3 3')
		arguments.append(output_folder)
		arguments.append(cluster_folder+f)

		command = 'python -u ' + dense_pipeline + ' '+' '.join(arguments) 
		if i%3 !=0:
			command+='&'
		print command
		os.system(command)

	i+=1
print 'done!'