import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<3:
	print 'bible_directory script_path'
	sys.exit(0)

fastalign =os.path.dirname(os.path.realpath(__file__))+'/fast_align.py'
bible_directory = os.path.abspath(sys.argv[1])+'/'
script_path = os.path.abspath(sys.argv[2])+'/'

commands = []
for f in os.listdir(bible_directory):
	langs = f.split('_')
	command = 'python -u '+fastalign+' '+  bible_directory+f + ' '+script_path+' '+langs[0]+' '+langs[1]
	commands.append(command)

counter = 0
while len(commands)>0:
	command = commands.pop()
	counter+=1
	if counter%20 != 0:
		command+='&'
	print command
	os.system(command)	
	print 'done!'
