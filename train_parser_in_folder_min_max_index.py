import os,sys,codecs
from collections import defaultdict

input_folder = os.path.abspath(sys.argv[1])+'/'
yara_jar = os.path.abspath(sys.argv[2])
brown_cluster_files = os.path.abspath(sys.argv[3])+'/'
output_folder = os.path.abspath(sys.argv[4])+'/'
min_index = int(sys.argv[5])
max_index = int(sys.argv[6])

commands = list()
i = 0
for f in os.listdir(input_folder):
	if i>=min_index and i<=max_index:
		print f
		command = 'nice java -jar ' + yara_jar+ ' train nt:4 iter:10 -train-file '+ input_folder+f +' -model '+output_folder+f + ' -cluster ' + brown_cluster_files+f + '&> /tmp/parse_log_'+f +'.tmp &'
		if len(commands)>=4:
			command = 'nice java -jar ' + yara_jar+ ' train nt:4 iter:10 -train-file '+ input_folder+f +' -model '+output_folder+f + ' -cluster ' + brown_cluster_files+f 
		commands.append(command)

		if len(commands)>=5:
			for c in commands:
				print c
				os.system(c)
			commands = list()	
	i+=1

for c in commands:
	os.system(c)


