import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<6:
	print 'run_giza_script giza_bin_path clean_script_path input_folder output_folder'
	sys.exit(0)

run_giza_script = os.path.abspath(sys.argv[1])
giza_bin_path = os.path.abspath(sys.argv[2])+'/'
clean_script_path = os.path.abspath(sys.argv[3])
input_folder = os.path.abspath(sys.argv[4])+'/'
output_folder = os.path.abspath(sys.argv[5])+'/'
min_c = int(sys.argv[6])
max_c = int(sys.argv[7])

langs = set()
for f in os.listdir(input_folder):
	if '.' in f:
		l = f[f.rfind('.')+1:]
		langs.add(l)

target_alignments = set()
for l1 in langs:
	for l2 in langs:
		if l1<l2:
			target_alignments.add(output_folder+l1+'_'+l2)

alignment_command_targets = list()
# creating alignment files
for t in target_alignments:
	if not os.path.exists(t):
		os.makedirs(t)

	l1 = t[t.rfind('/')+1:t.rfind('_')]
	l2 = t[t.rfind('_')+1:]
	if l1+'.'+l2 in os.listdir(input_folder):
		alignment_command_targets.append((t,input_folder+l1+'.'+l2,input_folder+l2+'.'+l1,l1,l2))
	else:
		print l1+'.'+l2, 'not found!'

counter = 0
while True:
	for i in range(0,11):
		if counter >= len(alignment_command_targets):
			break

		if counter>= min_c and counter<=max_c:
			command = 'nice python -u ' + run_giza_script +' '+ giza_bin_path + ' null '+clean_script_path + ' ' +alignment_command_targets[counter][0]+' '+ alignment_command_targets[counter][1]+' '+alignment_command_targets[counter][2]+ ' '+alignment_command_targets[counter][3]+ ' '+alignment_command_targets[counter][4]+ ' 1 100'
			if i<10:
				command+='&'
			
			print command
			os.system(command)	
		counter+=1

	if counter >= len(alignment_command_targets):
		break

print 'done!'




