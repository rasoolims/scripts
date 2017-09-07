import os,sys,codecs
from collections import defaultdict

input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'


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
	


	for i in xrange(ln):
		for s in labels.keys():
			if labels[s][i] == 'positive':
				pos_flat[i] += 1
			if labels[s][i] == 'negative':
				neg_flat[i] += 1
			if labels[s][i] == 'neutral':
				neut_flat[i] += 1

	writer_flat = codecs.open(output_folder+l,'w')

	for i in xrange(ln):
		if neut_flat[i]>pos_flat[i] and neut_flat[i]>neg_flat[i]:
			writer_flat.write(test_sens[l][i]+'\t'+'neutral\n')
		elif neg_flat[i]<pos_flat[i]:
			writer_flat.write(test_sens[l][i]+'\t'+'positive\n')
		else :
			writer_flat.write(test_sens[l][i]+'\t'+'negative\n')

		

	writer_flat.close()


