import os,sys

gold_conllu = open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')
auto_conllu = open(os.path.abspath(sys.argv[2]),'r').read().strip().split('\n\n')
writer = open(os.path.abspath(sys.argv[3]),'w')

assert len(auto_conllu)==len(gold_conllu)

for i in range(len(auto_conllu)):
	g_s = gold_conllu[i].strip().split('\n')
	a_s = auto_conllu[i].strip().split('\n')
	new_output = []

	j = 0
	for k in range(len(g_s)):
		spl = g_s[k].split('\t')
		if spl[0].isdigit():
			spl_auto = a_s[j].split('\t')
			spl[2] = spl_auto[2]
			spl[3] = spl_auto[3]
			spl[4] = spl_auto[4]
			new_output.append('\t'.join(spl))
			j+=1
		else:
			new_output.append(g_s[k].strip())
	writer.write('\n'.join(new_output)+'\n\n')
writer.close()

