import os,sys,codecs
from collections import defaultdict

input_folder = os.path.abspath(sys.argv[1])+'/'
pos_tagger_jar = os.path.abspath(sys.argv[2])
model_path = os.path.abspath(sys.argv[3])+'/'
output_folder = os.path.abspath(sys.argv[4])+'/'
delim = '_'
if len(sys.argv)>5:
	delim = sys.argv[5]
	if delim=='|||':
		delim = '\|\|\|'

print os.listdir(input_folder)
commands = list()
for f in os.listdir(input_folder):
	print f
	l = f
	if '_' in f:
		l = f[:f.find('_')]
	if '.' in l:
		l = l[l.rfind('.')+1:]
	command = 'nice java -jar ' + pos_tagger_jar+ ' tag -input '+ input_folder+f +' -model '+model_path+l + ' -output ' + output_folder+f + ' -delim '+delim +' &> /tmp/pos_log_'+f +'.tmp &'
	if len(commands)>=4:
		command = 'nice java -jar ' + pos_tagger_jar+ ' tag -input '+ input_folder+f +' -model '+model_path+l + ' -output ' + output_folder+f + ' -delim '+delim 
	commands.append(command)

	if len(commands)>=5:
		for c in commands:
			print c
			os.system(c)
		commands = list()

for c in commands:
	os.system(c)