import os,sys,codecs,operator
from collections import defaultdict

trees=codecs.open(sys.argv[1],'r').read().strip().split('\n\n')


sen_dict=dict()

for t in trees:
	spl=t.split('\n')
	if len(spl)<4:
		continue
	words=spl[0].split('\t')
	heads=spl[3].split('\t')

	dense_count=0
	for h in heads:
		if h!='-1':
			dense_count+=1

	density=float(dense_count)/len(words)

	sen=' '.join(words)

	sen_dict[sen]=density



sorted_x = sorted(sen_dict.items(), key=operator.itemgetter(1),reverse=True)

output=list()
for x in sorted_x:
	#print x
	output.append(x[0])



codecs.open(sys.argv[2],'w').write('\n'.join(output))