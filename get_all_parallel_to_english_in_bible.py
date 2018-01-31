import sys,os,codecs, random, pickle,gzip
from collections import defaultdict

bible_folder = os.path.abspath(sys.argv[1])+'/'
neg_dir = os.path.abspath(sys.argv[2])+'/'
output_path =  os.path.abspath(sys.argv[3]) 



en2dict = defaultdict(list)
print 'creating dictionaries'
for flat_dir in os.listdir(bible_folder):
	l1 = flat_dir[:flat_dir.rfind('_')]
	l2 = flat_dir[flat_dir.rfind('_')+1:]
	if l1 != 'en' and l2!='en':
		continue
	if l2 == 'en':
		l1,l2 = l2, l1

	f = bible_folder+flat_dir+'/'
	print f
	l1_tag = f + 'corpus.tok.clean.'+ l1 +'.conll.tag'
	l2_tag = f + 'corpus.tok.clean.'+ l2 +'.conll.tag'
	
	src_sens = codecs.open(l1_tag, 'r').read().strip().split('\n')
	dst_sens = codecs.open(l2_tag, 'r').read().strip().split('\n')

	assert len(src_sens) == len(dst_sens)
	for i in range(len(src_sens)):
		en2dict[src_sens[i]].append((l2, dst_sens[i]))

print len(en2dict)

print 'reading negative examples'
neg_examples = dict()

for f in os.listdir(neg_dir):
	lang = f[:-3]
	neg_examples[lang] = dict()
	print lang
	for line in gzip.open(neg_dir+f, 'r'):
		spl = line.strip().split('\t')
		sens = [spl[i].strip() for i in range(1, len(spl)-1, 2)]
		probs = [spl[i].strip() for i in range(2, len(spl), 2)]
		neg_examples[lang][sens[0]] = (sens, probs)

print 'writing data'
writer = codecs.open(output_path, 'w')
writer_dev = codecs.open(output_path+'.dev', 'w')

for en_sen in en2dict.keys():
	output = ['en', en_sen]
	neg_examples_ = neg_examples['en'][en_sen]
	len_ = len(neg_examples_[0])
	i_ = [random.randint(1, len_-1) for _ in range(min(5, len_-1))] 
	neg_sens = [neg_examples_[0][ind] for ind in i_]
	neg_ids = ['en' for _ in i_]

	to_dev = True if random.randint(0,9)==9 else False 
	for pr in en2dict[en_sen]:
		output.append(pr[0])
		output.append(pr[1])
		
		if not to_dev:
			neg_examples_ = neg_examples[pr[0]][pr[1]]
			len_ = len(neg_examples_[0])
			i_ = [random.randint(1, len_-1) for _ in range(min(5, len_-1))] 
			neg_sens = neg_sens + [neg_examples_[0][ind] for ind in i_]
			neg_ids = neg_ids + [pr[0] for _ in i_]

	if to_dev:
		writer_dev.write('\t'.join(output)+'\n')
	else:
		writer.write('\t'.join(output)+'\n')
		output = []
		for i in range(len(neg_sens)):
			output.append(neg_ids[i])
			output.append(neg_sens[i])
		writer.write('\t'.join(output)+'\n')

writer.close()
writer_dev.close()