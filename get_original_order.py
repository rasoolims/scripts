import os,sys,codecs

lines = codecs.open(os.path.abspath(sys.argv[1]), 'r').read().strip().split('\n')
outputs = []
for line in lines:
	l = len(line.strip().split())
	outputs.append(' '.join([str(i+1) for i in range(l)]))

writer =  open(os.path.abspath(sys.argv[2]), 'w').write('\n'.join(outputs)+'\n')