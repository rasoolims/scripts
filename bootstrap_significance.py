import os,sys,codecs, random
from collections import defaultdict


def f_score(g_lab, p_lab):
	tp = defaultdict(float)
	fp = defaultdict(float)
	fn = defaultdict(float)
	labels = set()
	for i in xrange(len(g_lab)):
		labels.add(g_lab[i])
		labels.add(p_lab[i])
		if p_lab[i]==g_lab[i]:
			tp[g_lab[i]]+=1
		else:
			fn[g_lab[i]]+=1
			fp[p_lab[i]]+=1


	mf = 0
	for lab in labels:
		p,r = 100.0*tp[lab]/(tp[lab]+fp[lab]) if (tp[lab]+fp[lab])>0 else 0 , 100.0*tp[lab]/(tp[lab]+fn[lab]) if (tp[lab]+fn[lab])>0 else 0
		f = 2*p*r /(p+r) if (p+r)>0 else 0
		mf+= f
	return float(mf)/len(labels)



g_lab = [line.split('\t')[1].strip() for line in open(os.path.abspath(sys.argv[1]),'r')]
p1_lab = [line.split('\t')[1].strip()  for line in open(os.path.abspath(sys.argv[2]),'r')]
p2_lab = [line.split('\t')[1].strip()  for line in open(os.path.abspath(sys.argv[3]),'r')]

b = 1000000
l = len(g_lab)
sample_size = l/3

orig_f_1 = f_score(g_lab, p1_lab)
orig_f_2 = f_score(g_lab, p2_lab)


print 'original difference', orig_f_1 - orig_f_2
two_delta = 2*(orig_f_1 - orig_f_2)

s = 0
for i in xrange(b):
	g_sample = []
	p1_sample = []
	p2_sample = []

	for _ in xrange(sample_size):
		r = random.randint(0, l-1)
		g_sample.append(g_lab[r]) 
		p1_sample.append(p1_lab[r])
		p2_sample.append(p2_lab[r])

	f_1 = f_score(g_sample, p1_sample)
	f_2 = f_score(g_sample, p2_sample)
	diff = f_1 - f_2
	if diff> two_delta:
		s+=1 

	if i%1000==0:
		sys.stdout.write(str(i)+'...')

sys.stdout.write('\n')

print float(s)/b

