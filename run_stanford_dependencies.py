import os,sys

#java -cp stanford-parser-v1.6.8.jar -Xmx20g    edu.stanford.nlp.trees.EnglishGrammaticalStructure  -treeFile ../../../LDC2013T19-OntoNotesRelease5.0/parse    -conllx -basic -makeCopulaHead -keepPunct > ../../../LDC2013T19-OntoNotesRelease5.0/parse.conll

stanford_path=os.path.abspath(sys.argv[1])
path=os.path.abspath(sys.argv[2])

commands=list()
os.chdir(os.path.dirname(stanford_path))
for root, dirs, files in os.walk(path):
	for name in files:
		if name.endswith(".parse"):
			full_path=root+'/'+name
			
			output_path=full_path+'.conll'
			command='java -cp '+stanford_path+' -Xmx2g edu.stanford.nlp.trees.EnglishGrammaticalStructure  -treeFile ' +\
			full_path+' -conllx basic makeCopulaHead -keepPunct > '+output_path 
			commands.append(command)
			if len(commands)>30:
				for i in range(0,len(commands)-1):
					os.system(commands[i] + ' &')
				os.system(commands[len(commands)-1])
				commands=list()
			print output_path
print 'done!'