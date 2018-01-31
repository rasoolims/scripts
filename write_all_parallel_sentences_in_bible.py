import sys,os,codecs, random, pickle
from collections import defaultdict

unique_folder = os.path.abspath(sys.argv[1])+'/'
bible_folder = os.path.abspath(sys.argv[2])+'/'
output_path =  os.path.abspath(sys.argv[3]) 

writer = codecs.open(output_path, 'w')

print 'creating dictionaries'
sentence_dict = dict()
for l in os.listdir(unique_folder):
	sentence_dict[l] = dict()
	print l
	for line in codecs.open(unique_folder+l, 'r'):
		if not line.strip() in sentence_dict[l]:
			sentence_dict[l][line.strip()] = len(sentence_dict[l])
pickle.dump(sentence_dict, open(output_path+'.dict', "wb"))

print 'creating corpus'
for flat_dir in os.listdir(bible_folder):
	l1 = flat_dir[:flat_dir.rfind('_')]
	l2 = flat_dir[flat_dir.rfind('_')+1:]
	f = bible_folder+flat_dir+'/'
	print f
	l1_tag = f + 'corpus.tok.clean.'+ l1 +'.conll.tag'
	l2_tag = f + 'corpus.tok.clean.'+ l2 +'.conll.tag'
	
	src_sens = codecs.open(l1_tag, 'r').read().strip().split('\n')
	dst_sens = codecs.open(l2_tag, 'r').read().strip().split('\n')

	assert len(src_sens) == len(dst_sens)
	for i in range(len(src_sens)):
		writer.write('\t'.join([l1, l2, str(sentence_dict[l1][src_sens[i]]), str(sentence_dict[l2][dst_sens[i]])])+'\n')

writer.close()