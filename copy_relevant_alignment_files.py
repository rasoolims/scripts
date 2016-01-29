import os,sys,codecs,random


in_path = os.path.abspath(os.path.dirname(sys.argv[1]))+'/'
out_path = os.path.abspath(os.path.dirname(sys.argv[2]))+'/'

langs = ['English','German','Japanese','Korean','Indonesian','Spanish','French','Italian','Portuguese','Swedish']

for l1 in langs:
	for l2 in langs:
		if l1==l2: continue
		command = 'cp '+in_path+l1+'_'+l2+'.'+l1 +' '+out_path+' '
		print command
		os.system(command)
print 'done'