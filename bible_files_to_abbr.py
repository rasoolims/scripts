import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<3:
	print 'input_folder  output_folder '
	sys.exit(0)
input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'

langs = {'Arabic':'ar','Farsi':'fa','English':'en','Chinese-tok':'zh','Polish':'pl','Swedish':'sv','Croatian':'hr',
		'Bulgarian':'bg','German':'de','English':'en','Russian':'ru','Spanish':'es','Slovene':'sl','Slovak':'sk',
		'Hungarian':'hu','Portuguese':'pt'}

commands = list()
for f in os.listdir(input_folder):
	dest = f.split('.')[1]
	source = f.split('.')[0].split('_')[1]

	if dest!=source and dest in langs and source in langs:
		dest = langs[dest]
		source = langs[source]
		nf = source+'.'+dest
		command= 'cp '+input_folder+f +' '+output_folder+nf
		print command
		os.system(command)
