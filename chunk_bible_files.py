import os,sys
from collections import defaultdict

if len(sys.argv)<5:
	print 'python_script_path model_path bible_folder langs(separated by ,)'
	sys.exit(0)

python_script = os.path.abspath(sys.argv[1])
model_folder =  os.path.abspath(sys.argv[2])+'/'
input_folder =  os.path.abspath(sys.argv[3])+'/'
langs = sys.argv[4].strip().split(',')

files = defaultdict(list)

for d in sorted(os.listdir(input_folder)):
	folder = input_folder+d+'/'
	for f in sorted(os.listdir(folder)):
		for lang in langs:
			if f == 'corpus.tok.clean.'+lang:
				files[lang].append(folder+f)

print files

commands = []
for lang in files.keys():
	command = 'nice python -u '+python_script+' --model '+ model_folder+lang+'/chunk/model.model --params  '+ model_folder+lang+'/chunk/params.pickle --pos_model  '+ model_folder+lang+'/pos/model.model --pos_params  '+ model_folder+lang+'/pos/params.pickle --inputs '+','.join(files[lang])
	if len(commands)<4:
		command += '&'
	commands.append(command)
	if len(commands)>=5:
		for c in commands:
			print c
			os.system(c)
		commands = list()
	
for c in commands:
	print c
	os.system(c)
commands = list()
