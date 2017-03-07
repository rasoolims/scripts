import os,sys,codecs
from collections import defaultdict

input_folder = os.path.abspath(sys.argv[1])+'/'
sim_file = os.path.abspath(sys.argv[2])
output_folder = os.path.abspath(sys.argv[3])+'/'

cos_sims = defaultdict(dict)
kl_sims = defaultdict(dict)

print 'reading simalarities'
for line in open(sim_file):
	s,t,kl,sim = line.strip().split()
	cos_sims[s][t] = float(sim)
	kl_sims[s][t] = float(kl)*float(kl)



langs_files =defaultdict(set)
test_sens = defaultdict()
for f in os.listdir(input_folder):
	l1,l2 = f.split('2')[0],f.split('2')[1]
	langs_files[l2].add(f)

for l in langs_files.keys():
	print l
	labels = defaultdict()
	ln = 0
	for f in langs_files[l]:
		s = f.split('2')[0]
		labels[s] = list()
		test_sens[l] = list()
		for line in codecs.open(input_folder+f,'r'):
			if line.strip():
				labels[s].append(line.strip().split('\t')[1])
				test_sens[l].append(line.strip().split('\t')[0])
		ln = len(labels[s])


	pos_flat = [0]*ln
	neg_flat = [0]*ln
	neut_flat = [0]*ln
	
	pos_kl = [0.0]*ln
	neg_kl = [0.0]*ln
	neut_kl = [0.0]*ln

	pos_cos = [0.0]*ln
	neg_cos = [0.0]*ln
	neut_cos = [0.0]*ln


	for i in xrange(ln):
		for s in labels.keys():
			kl_sim = kl_sims[l][s]
			cos_sim = cos_sims[l][s]

			if labels[s][i] == 'positive':
				pos_flat[i] += 1
				pos_kl[i] += kl_sim
				pos_cos[i] += cos_sim
			if labels[s][i] == 'negative':
				neg_flat[i] += 1
				neg_kl[i] += kl_sim
				neg_cos[i] += cos_sim
			if labels[s][i] == 'neutral':
				neut_flat[i] += 1
				neut_kl[i] += kl_sim
				neut_cos[i] += cos_sim

	writer_flat = codecs.open(output_folder+l+'.flat','w')
	writer_cos = codecs.open(output_folder+l+'.cos','w')
	writer_kl = codecs.open(output_folder+l+'.kl','w')

	for i in xrange(ln):
		if neut_flat[i]>pos_flat[i] and neut_flat[i]>neg_flat[i]:
			writer_flat.write(test_sens[l][i]+'\t'+'neutral\n')
		elif neg_flat[i]<pos_flat[i]:
			writer_flat.write(test_sens[l][i]+'\t'+'positive\n')
		else:
			writer_flat.write(test_sens[l][i]+'\t'+'negative\n')

		if neut_kl[i]>pos_kl[i] and neut_kl[i]>neg_kl[i]:
			writer_kl.write(test_sens[l][i]+'\t'+'neutral\n')
		elif neg_kl[i]<pos_kl[i]:
			writer_kl.write(test_sens[l][i]+'\t'+'positive\n')
		else:
			writer_kl.write(test_sens[l][i]+'\t'+'negative\n')


		if neut_cos[i]>pos_cos[i] and neut_cos[i]>neg_cos[i]:
			writer_cos.write(test_sens[l][i]+'\t'+'neutral\n')
		elif neg_cos[i]<pos_cos[i]:
			writer_cos.write(test_sens[l][i]+'\t'+'positive\n')
		else:
			writer_cos.write(test_sens[l][i]+'\t'+'negative\n')

	writer_flat.close()
	writer_cos.close()
	writer_kl.close()


