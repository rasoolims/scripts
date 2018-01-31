import sys,os,codecs, random, pickle,gzip
from collections import defaultdict

bible_folder = os.path.abspath(sys.argv[1])+'/'
output_path =  os.path.abspath(sys.argv[2]) 

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


print 'writing data'
writer = codecs.open(output_path, 'w')
writer_dev = codecs.open(output_path+'.dev', 'w')

for en_sen in en2dict.keys():
	output = ['en', en_sen]
	

	to_dev = True if random.randint(0,9)==9 else False 
	for pr in en2dict[en_sen]:
		output.append(pr[0])
		output.append(pr[1])
		

	if to_dev:
		writer_dev.write('\t'.join(output)+'\n')
	else:
		writer.write('\t'.join(output)+'\n')

writer.close()
writer_dev.close()