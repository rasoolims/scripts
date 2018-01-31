import sys,os,codecs, random
from collections import defaultdict

source_lang = sys.argv[1]
target_lang = sys.argv[2]
source_sentences = codecs.open(os.path.abspath(sys.argv[3]),'r').read().strip().split('\n')
target_sentences = codecs.open(os.path.abspath(sys.argv[4]),'r').read().strip().split('\n') 
target_words = dict()
bin_info = defaultdict(list)
for line in codecs.open(os.path.abspath(sys.argv[5]),'r'):
	f = line.strip().split()
	if len(f)==3:
		word, prob, bin = f[0], float(f[1]), int(f[2])
		bin_info[bin].append(f[0])
		target_words[word] = (prob, bin)


k = int(sys.argv[6])
output_writer = codecs.open(os.path.abspath(sys.argv[7]),'w')

assert len(source_sentences) == len(target_sentences)


for i in range(len(source_sentences)):
	output = list()
	output.append(source_lang)
	output.append(target_lang)

	output.append(source_sentences[i])
	output.append(target_sentences[i])
	words, tags = [], []
	
	for spl in target_sentences[i].strip().split():
		tind = spl.rfind('_')
		words.append(spl[:tind])
		tags.append(spl[tind+1:])

	rw = random.randint(0, len(words)-1)
	prob = target_words[words[rw]][0] if words[rw] in target_words else 1e-10
	output.append(str(prob))

	for j in range(len(words)):
		sample = [w for w in words]
		bin_number = target_words[sample[j]][1] if sample[j] in target_words else 0

		if bin_number>0:
			tw = bin_info[bin_number]
			for k_ in range(k):
				r = random.randint(0, len(tw)-1)
				sample[j] = tw[r]
				prob = target_words[sample[j]][0]

				new_output = ' '.join([sample[f]+'_'+tags[f] for f in range(len(words))]) + '\t'+ str(prob)
				output.append(new_output)

	output_writer.write('\t'.join(output)+'\n')
	if (i+1)%100==0:
		sys.stdout.write(str(i+1)+'...')

output_writer.close()
