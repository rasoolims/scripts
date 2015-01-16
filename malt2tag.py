import os,codecs,sys


sentences=codecs.open(os.path.abspath(sys.argv[1]),'r').read().split('\n\n')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')

for sen in sentences:
	ln=sen.strip().split('\n')
	output=list()
	for l in ln:
		flds=l.split('\t')
		if len(flds)>3:
			output.append(flds[0]+'_'+flds[1])
	writer.write(' '.join(output)+'\n')

writer.flush()

