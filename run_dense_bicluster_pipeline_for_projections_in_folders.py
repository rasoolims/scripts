import os,sys,codecs
from collections import defaultdict

dense_pipeline = os.path.dirname(os.path.abspath(sys.argv[0]))+'/dense_pipeline_bicluster_no_eval.py'

jar_file = os.path.abspath(sys.argv[1])
cluster_id_folder = os.path.abspath(sys.argv[2])+'/'
cluster_path = os.path.abspath(sys.argv[3])
folder_full = os.path.abspath(sys.argv[4])+'/'
folder_par7 = os.path.abspath(sys.argv[5])+'/'
folder_par5 = os.path.abspath(sys.argv[6])+'/'
folder_par1 = os.path.abspath(sys.argv[7])+'/'
output_folder = os.path.abspath(sys.argv[8])+'/'
min_cnt = int(sys.argv[9])
max_cnt = int(sys.argv[10])

i = 0
counter = 0
for f in sorted(os.listdir(folder_full)):
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
		arguments.append(cluster_id_folder+f)
		arguments.append(cluster_path)
		counter+=1

		command = 'python -u ' + dense_pipeline + ' '+' '.join(arguments) + ' > /tmp/'+f+'.out '
		if counter%3 !=0:
			command+='&'
		print command
		os.system(command)

	i+=1
print 'done!'