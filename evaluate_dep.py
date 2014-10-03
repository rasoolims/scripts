import os,sys,codecs

gold_sens=codecs.open(os.path.abspath(sys.argv[1]),'r').read().split('\n\n')
auto_sens=codecs.open(os.path.abspath(sys.argv[2]),'r').read().split('\n\n')

if len(gold_sens)!=len(auto_sens):
	print len(gold_sens),len(auto_sens)
	sys.exit(0)
