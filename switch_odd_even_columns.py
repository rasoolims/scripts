import os,sys,codecs,operator

sens=codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n')
for sen in sens:
	spl = sen.strip().split('&')
	#print spl
	for i in range(2,len(spl),2):
		tmp = spl[i]
		spl[i] = spl[i+1]
		spl[i+1] = tmp
	#print spl
	print ' & '.join(spl) + ' \\\\ \\hline '