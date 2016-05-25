import os,sys,codecs
from collections import defaultdict

input_folder = os.path.abspath(sys.argv[1])+'/'
yara_jar = os.path.abspath(sys.argv[2])
model_path = os.path.abspath(sys.argv[3])+'/'
output_folder = os.path.abspath(sys.argv[4])+'/'

print os.listdir(input_folder)
commands = list()
for f in os.listdir(input_folder):
	print f
	command = 'nice java -jar ' + yara_jar+ ' parse_tagged nt:2 -input '+ input_folder+f +' -model '+model_path+f + ' -output ' + output_folder+f + '&> /tmp/parse_log_'+f +'.tmp &'
	if len(commands)>=4:
		command = 'nice java -jar ' + yara_jar+ ' parse_tagged nt:2 -input '+ input_folder+f +' -model '+model_path+f + ' -output ' + output_folder+f 
	commands.append(command)

	if len(commands)>=5:
		for c in commands:
			print c
			os.system(c)
		commands = list()

for c in commands:
	os.system(c)