import os,sys,codecs
from collections import defaultdict

input_folder = os.path.abspath(sys.argv[1])+'/'
pos_tagger_jar = os.path.abspath(sys.argv[2])
model_path = os.path.abspath(sys.argv[3])+'/'
delim = '_'
if len(sys.argv)>5:
	delim = sys.argv[5]
	if delim=='|||':
		delim = '\|\|\|'

print os.listdir(input_folder)
commands = list()
for f in os.listdir(input_folder):
	if not os.path.isdir(input_folder+f): continue
	print f
	l1 = f[:f.find('_')]
	l2 = f[f.find('_')+1:]
	f1 = input_folder+'/'+f+'/corpus.tok.clean.'+l1
	f2 = input_folder+'/'+f+'/corpus.tok.clean.'+l2
	of1 = input_folder+'/'+f+'/corpus.tok.clean.tag.'+l1
	of2 = input_folder+'/'+f+'/corpus.tok.clean.tag.'+l2

	command = 'nice java -jar ' + pos_tagger_jar+ ' tag -input '+ f1 +' -model '+model_path+l1 + ' -output ' + of1 + ' -delim '+delim 
	if len(commands)<9:
		command+=' &'
	commands.append(command)

	command = 'nice java -jar ' + pos_tagger_jar+ ' tag -input '+ f2 +' -model '+model_path+l2 + ' -output ' + of2 + ' -delim '+delim 
	if len(commands)<9:
		command+=' &'
	commands.append(command)

	if len(commands)>=10:
		for c in commands:
			print c
			os.system(c)
		commands = list()

for c in commands:
	os.system(c)