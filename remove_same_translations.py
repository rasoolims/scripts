import os,sys,codecs

if len(sys.argv)<4:
	print '[src_lang_file] [target_lang_file] [src_lang_output] [target_lang_output]'
	sys.exit(0)

s_sens = codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n')
t_sens = codecs.open(os.path.abspath(sys.argv[2]),'r').read().strip().split('\n')

assert len(s_sens) == len(t_sens)

writer1 = codecs.open(os.path.abspath(sys.argv[3]),'w')
writer2 = codecs.open(os.path.abspath(sys.argv[4]),'w')

for i in xrange(len(s_sens)):
	if s_sens[i].strip()==t_sens[i].strip():
		print s_sens[i]
	else:
		writer1.write(s_sens[i].strip()+'\n')
		writer2.write(t_sens[i].strip()+'\n')
writer1.close()
writer2.close()