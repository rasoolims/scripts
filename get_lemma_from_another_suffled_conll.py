import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<3:
	print 'input_file output_file'
	sys.exit(0)

print 'reading content'
new_file = codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')
old_file = codecs.open(os.path.abspath(sys.argv[2]),'r').read().strip().split('\n\n')
writer = codecs.open(os.path.abspath(sys.argv[3]),'w')

sentences = dict()
lemma_dict = dict()

print 'creating lemma dictionary'
c = 0
for of in old_file:
	lines = of.strip().split('\n')
	o_s = []
	o_l = []
	for line in lines:
		spl = line.strip().split('\t')
		o_s.append(spl[1])
		o_l.append(spl[2])
		lemma_dict[spl[1]]=spl[2]
	c+=1
	sentences[' '.join(o_s)] = ' '.join(o_l)
	if c%10000 == 0:
		sys.stdout.write(str(c)+'...')
sys.stdout.write('!\n')

c = 0
f = 0
for nf in new_file:
	lines = nf.strip().split('\n')
	o_s = []
	for line in lines:
		spl = line.strip().split('\t')
		o_s.append(spl[1])
	sentence = ' '.join(o_s)
	lemmas = []
	if sentence in sentences:
		f+=1
		lemmas = sentences[sentence].split()
	else:
		for w in o_s:
			if w in lemma_dict:
				lemmas.append(lemma_dict[w])
			else:
				lemmas.append(w)
	
	for i in xrange(len(lines)):
		spl = lines[i].strip().split('\t')
		spl[2] = lemmas[i]
		writer.write('\t'.join(spl)+'\n')
	writer.write('\n')

	c+=1
	if c%10000 == 0:
		sys.stdout.write(str(c)+'('+str(f)+')'+'...')

writer.close()
sys.stdout.write('!\n')


