import os,sys,random

g_sen = [line.split('\t')[0].strip() for line in open(os.path.abspath(sys.argv[1]),'r')]
g_lab = [line.split('\t')[1].strip() for line in open(os.path.abspath(sys.argv[1]),'r')]
p1_lab = [line.split('\t')[1].strip()  for line in open(os.path.abspath(sys.argv[2]),'r')]
p2_lab = [line.split('\t')[1].strip()  for line in open(os.path.abspath(sys.argv[3]),'r')]
sup_lab = [line.split('\t')[1].strip()  for line in open(os.path.abspath(sys.argv[4]),'r')]

writer = open(os.path.abspath(sys.argv[5]),'w')

outputs = []
for i in xrange(len(g_sen)):
	if p1_lab[i] != g_lab[i] or p2_lab[i]!=g_lab[i]:
		outputs.append(g_sen[i]+'\t'+p1_lab[i]+'\t'+p2_lab[i]+'\t'+sup_lab[i]+'\t'+g_lab[i])


samples = random.sample(outputs, 100)

writer.write('\n'.join(samples))
writer.close()