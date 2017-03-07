import os,sys,codecs
from collections import defaultdict

input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'

sim_langs = {'ar':['ct','pr','en'], 'bg':['ct','pr','en'], 'de':['ct','pr','en'], 'en':['ct','pr','de'],
			'es':['ct','pr','en'], 'fa':['ct','pr','en'], 'hr':['ct','pr','en'], 'hu':['ct','pr','en'],
			'pl':['ct','pr','en'], 'pt':['ct','pr','en'], 'ru':['ct','pr','en'], 'sk':['ct','pr','en'],
			'sl':['ct','pr','en'], 'sv':['ct','pr','en'], 'ug':['ct','pr','en'], 'zh':['ct','pr','en']}


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

	two_best = 0
	two_best_dict = defaultdict(int)
	for i in xrange(ln):
		has_two_best = False
		if neg_flat[i]>pos_flat[i] and neg_flat[i]>neut_flat[i]:
			writer_flat.write(test_sens[l][i]+'\t'+'negative\n')
		elif neut_flat[i]<pos_flat[i]:
			has_res = False
			if neg_flat[i]==pos_flat[i]:
				two_best_dict['p,ng']+=1
				has_two_best= True

				for lang in sim_langs[l]:
					if not lang in labels:
						continue
					if labels[lang][i] == 'positive':
						writer_flat.write(test_sens[l][i]+'\t'+'positive\n')
						has_res = True
						break
					elif labels[lang][i] == 'negative':
						writer_flat.write(test_sens[l][i]+'\t'+'negative\n')
						has_res = True
						break
			else:
				writer_flat.write(test_sens[l][i]+'\t'+'positive\n')

			if has_two_best and not has_res:
				writer_flat.write(test_sens[l][i]+'\t'+'positive\n')
		else:
			has_res = False
			if neut_flat[i]==pos_flat[i]: 
				has_two_best= True
				two_best_dict['p,nt']+=1
				for lang in sim_langs[l]:
					if not lang in labels:
						continue
					if labels[lang][i] == 'positive':
						writer_flat.write(test_sens[l][i]+'\t'+'positive\n')
						has_res = True
						break
					elif labels[lang][i] == 'neutral':
						writer_flat.write(test_sens[l][i]+'\t'+'neutral\n')
						has_res = True
						break
			elif neut_flat[i]==neg_flat[i] and not has_res:
				has_two_best= True
				two_best_dict['ng,nt']+=1
				for lang in sim_langs[l]:
					if not lang in labels:
						continue
					if labels[lang][i] == 'negative':
						writer_flat.write(test_sens[l][i]+'\t'+'negative\n')
						has_res = True
						break
					elif labels[lang][i] == 'neutral':
						writer_flat.write(test_sens[l][i]+'\t'+'neutral\n')
						has_res = True
						break
			else:
				writer_flat.write(test_sens[l][i]+'\t'+'neutral\n')
			if has_two_best and not has_res:
				writer_flat.write(test_sens[l][i]+'\t'+'neutral\n')
		if has_two_best: two_best+=1

	print two_best, float(two_best)/ln
	print two_best_dict




	writer_flat.close()
