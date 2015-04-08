import os,sys,codecs


sens=codecs.open(os.path.abspath(sys.argv[1]),'r').read().split('\n')

output=list()

for sen in sens:
	if not sen.strip():
		continue
	o=list()
	spl=sen.strip().split(' ')
	for s in spl:
		wt=s.split('_')
		if wt[1]=='***':
			o.append(wt[0])
		else:
			o.append(wt[0]+' '+wt[1])
	output.append('\n'.join(o))

codecs.open(os.path.abspath(sys.argv[2]),'w').write('\n\n'.join(output))
