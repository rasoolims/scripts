import sys,os,codecs, random, pickle, gzip
from collections import defaultdict


print 'reading sentence dictionary'

sentence_dict = pickle.load(open(os.path.abspath(sys.argv[1]),'r'))
rev_sen_map = dict()
for l in sentence_dict.keys():
	rev_sen_map[l] = ['' for _ in range(len(sentence_dict[l]))]
	for sen in sentence_dict[l].keys():
		rev_sen_map[l][sentence_dict[l][sen]] = sen

print 'reading parallel data'
par_data = list()
for line in gzip.open(os.path.abspath(sys.argv[2]), 'r'):
	spl = line.strip().split()
	par_data.append([spl[0], spl[1], int(spl[2]), int(spl[3])])

print 'shuffling the parallel data'
random.shuffle(par_data)

split_point = (9*len(par_data))/10
train_data = par_data[:split_point]
dev_data = par_data[split_point:]

print 'writing dev data'
dev_writer = codecs.open(os.path.abspath(sys.argv[4]),'w')
for d in dev_data:
	l1, l2, id1, id2 = d
	sen1, sen2 = rev_sen_map[l1][id1], rev_sen_map[l2][id2]
	dev_writer.write('\t'.join([l1,l2,sen1,sen2])+'\n')
dev_writer.close()

print 'reading negative examples'
neg_dir = os.path.abspath(sys.argv[3])+'/'
neg_examples = dict()

for f in os.listdir(neg_dir):
	lang = f[:-3]
	neg_examples[lang] = dict()
	print lang
	for line in gzip.open(neg_dir+f, 'r'):
		spl = line.strip().split('\t')
		sens = [spl[i].strip() for i in range(1, len(spl)-1, 2)]
		probs = [spl[i].strip() for i in range(2, len(spl), 2)]
		sen_id = sentence_dict[lang][sens[0]] 
		neg_examples[lang][sen_id] = (sens, probs)


print 'creating training data parts'
directory_path = os.path.abspath(sys.argv[5])+'/'
part_number = 1
print len(train_data)
for i in range(1, 21):
	print '\nround', str(i)
	output = []
	for i_d, d in enumerate(train_data):
		l1, l2, id1, id2 = d
		neg_examples_l1 = neg_examples[l1][id1]
		neg_examples_l2 = neg_examples[l2][id2]
		len1, len2 = len(neg_examples_l1[0]), len(neg_examples_l2[0])
		i1 = [0] + [random.randint(1, len1-1) for _ in range(min(5, len1-1))] 
		i2 = [0] + [random.randint(1, len2-1) for _ in range(min(5, len2-1))]
		sens1 = [neg_examples_l1[0][ind] for ind in i1]
		sens2 = [neg_examples_l2[0][ind] for ind in i2]
		probs1 = [neg_examples_l1[1][ind] for ind in i1]
		probs2 = [neg_examples_l2[1][ind] for ind in i2]

		output.append('\t'.join([l1,l2, sens1[0], sens2[0], probs1[0], '1']))
		for i in range(1, len(sens2)):
			output.append('\t'.join([l1,l2, sens1[0], sens2[i], probs2[i], '0']))
		for i in range(1, len(sens1)):
			output.append('\t'.join([l1,l2, sens1[i], sens2[0], probs1[i], '0']))
		
		if len(output)>=1000:
			codecs.open(directory_path+'part_'+str(part_number),'w').write('\n'.join(output))
			os.system('gzip '+directory_path+'part_'+str(part_number) + ' &')
			part_number+=1
			if part_number%100==0:
				sys.stdout.write(str(part_number)+'/'+str(i_d+1)+'...')
			output = []

	random.shuffle(train_data)

print 'done!'
