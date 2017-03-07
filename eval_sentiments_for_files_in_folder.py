import os,sys,codecs
from collections import defaultdict

def get_acc(gold, predicted):
	g_lab = [line.split('\t')[1].strip() for line in codecs.open(gold,'r')]
	p_lab = [line.split('\t')[1].strip() for line in codecs.open(predicted,'r')]
	correct = len([1 for i in xrange(len(g_lab)) if g_lab[i]==p_lab[i]])
	return 100*float(correct)/len(g_lab)


input_folder = os.path.abspath(sys.argv[1])+'/'
test_folder = os.path.abspath(sys.argv[2])+'/'
writer = open(os.path.abspath(sys.argv[3]),'w')

langs=set()
accs = defaultdict(dict)
for f in os.listdir(input_folder):
	print f
	l1,l2 = f.split('2')[0],f.split('2')[1]
	langs.add(l1)
	langs.add(l2)

	acc = get_acc(test_folder+l2, input_folder+f)
	accs[l1][l2] = acc

output = []
o = ['-']
for s in sorted(accs.keys()):
	o.append(s)
output.append(' '.join(o))
for lang in sorted(langs):
	o = [lang]
	for s in sorted(accs.keys()):
		if lang in accs[s]:
			o.append(str(round(accs[s][lang],1)))
		else:
			o.append('--')
	output.append(' '.join(o))
writer.write('\n'.join(output))
writer.close()
