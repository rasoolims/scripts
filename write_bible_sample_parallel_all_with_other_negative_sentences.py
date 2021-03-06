import sys,os,codecs, random, pickle,gzip
from collections import defaultdict

bible_folder = os.path.abspath(sys.argv[1])+'/'
output_path =  os.path.abspath(sys.argv[2]) 

lang_sentences_set = defaultdict(set)
langs = set()
en2dict = defaultdict(list)
print 'creating dictionaries'
for flat_dir in os.listdir(bible_folder):
	l1 = flat_dir[:flat_dir.rfind('_')]
	l2 = flat_dir[flat_dir.rfind('_')+1:]
	if l1 != 'en' and l2!='en':
		continue
	if l2 == 'en':
		l1,l2 = l2, l1
	langs.add(l1)
	langs.add(l2)

	f = bible_folder+flat_dir+'/'
	print f
	l1_tag = f + 'corpus.tok.clean.'+ l1 +'.conll.tag'
	l2_tag = f + 'corpus.tok.clean.'+ l2 +'.conll.tag'
	
	src_sens = codecs.open(l1_tag, 'r').read().strip().split('\n')
	dst_sens = codecs.open(l2_tag, 'r').read().strip().split('\n')

	assert len(src_sens) == len(dst_sens)
	for i in range(len(src_sens)):
		lang_sentences_set[l1].add(src_sens[i])
		lang_sentences_set[l2].add(dst_sens[i])
		en2dict[src_sens[i]].append((l2, dst_sens[i]))

neg_examples = defaultdict(list)
for lang in lang_sentences_set.keys():
	neg_examples[lang] = list(lang_sentences_set[lang])
	print lang, len(neg_examples[lang])


print len(en2dict)


print 'writing data'
writer = codecs.open(output_path, 'w')
writer_dev = codecs.open(output_path+'.dev', 'w')

langs = list(langs)

for en_sen in en2dict.keys():
	to_dev = True if random.randint(0,100)==100 else False 
	langs_to_use = set([langs[random.randint(0, len(langs)-1)] for _ in range(2)])
	# print langs_to_use

	output = []
	if 'en' in langs_to_use or to_dev:
		output = ['en', en_sen]

	neg_examples_ = neg_examples['en']
	len_ = len(neg_examples_)
	i_ = [random.randint(1, len_-1) for _ in range(5)] 
	
	neg_sens = []
	neg_ids = []

	if 'en' in langs_to_use:
		neg_sens = [neg_examples_[ind] for ind in i_]
		neg_ids = ['en' for _ in i_]

	for pr in en2dict[en_sen]:
		if to_dev:
			output.append(pr[0])
			output.append(pr[1])
		elif pr[0] in langs_to_use:
			output.append(pr[0])
			output.append(pr[1])
			neg_examples_ = neg_examples[pr[0]]
			len_ = len(neg_examples_)
			i_ = [random.randint(1, len_-1) for _ in range(5)] 
			neg_sens = neg_sens + [neg_examples_[ind] for ind in i_]
			neg_ids = neg_ids + [pr[0] for _ in i_]

	if to_dev:
		writer_dev.write('\t'.join(output)+'\n')
	else:
		if len(output)>=4: # at least two positive examples.
			writer.write('\t'.join(output)+'\n')
			output = []
			assert len(neg_sens) == len(neg_ids)
			assert len(neg_sens)>0
			for i in range(len(neg_sens)):
				output.append(neg_ids[i])
				output.append(neg_sens[i])
			writer.write('\t'.join(output)+'\n')

writer.close()
writer_dev.close()