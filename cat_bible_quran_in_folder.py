import os,sys,codecs

if len(sys.argv)<3:
	print 'bible_folder  quran_folder  output_folder'
	sys.exit(0)
bible_folder = os.path.abspath(sys.argv[1])+'/'
quran_folder = os.path.abspath(sys.argv[2])+'/'
output_folder = os.path.abspath(sys.argv[3])+'/'

bible_files = set(os.listdir(bible_folder))
quran_files = set(os.listdir(quran_folder))
files = set(os.listdir(bible_folder)+os.listdir(quran_folder))


for f in files:
	if f in bible_files and f in quran_files:
		command = 'cat '+bible_folder+f+' '+quran_folder+f+' > '+output_folder+f
	elif f in quran_files:
		command = 'cp '+quran_folder+f+' '+output_folder+f
	else:
		command = 'cp '+bible_folder+f+' '+output_folder+f
	print command
	os.system(command)

