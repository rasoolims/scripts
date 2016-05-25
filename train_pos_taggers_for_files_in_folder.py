import os,sys,codecs
from collections import defaultdict

input_folder = os.path.abspath(sys.argv[1])+'/'
pos_tagger_jar = os.path.abspath(sys.argv[2])
brown_cluster_files = os.path.abspath(sys.argv[3])+'/'
output_folder = os.path.abspath(sys.argv[4])+'/'


commands = list()
for f in os.listdir(input_folder):
	print f
	command = 'nice java -jar ' + pos_tagger_jar+ ' train -update:early iter:15 -input '+ input_folder+f +' -model '+output_folder+f + ' -cluster ' + brown_cluster_files+f + '&> /tmp/pos_log_'+f +'.tmp &'
	if len(commands)>=4:
		command = 'nice java -jar ' + pos_tagger_jar+ ' train -update:early iter:15 -input '+ input_folder+f +' -model '+output_folder+f + ' -cluster ' + brown_cluster_files+f 
	commands.append(command)

	if len(commands)>=5:
		for c in commands:
			print c
			os.system(c)
		commands = list()

for c in commands:
	os.system(c)


