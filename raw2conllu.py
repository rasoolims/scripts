import os,sys,codecs

writer = codecs.open(os.path.abspath(sys.argv[2]),'w')
c = 0
for line in codecs.open(os.path.abspath(sys.argv[1]),'r'):
	words = line.strip().split()
	c+=1
	if c%10000==0: sys.stdout.write(str(c)+'...')
	for i in xrange(len(words)):
		output = str(i+1)+'\t' + words[i]+'\t'+'\t'.join(['_']*8)+'\n'
		writer.write(output)
	writer.write('\n')
sys.stdout.write(str(c)+'\n')
writer.close()