import os,sys,codecs,random
from collections import defaultdict
from random import randint

langs = set(['de','fr','es','it','pt','sv'])

main_directory = os.path.abspath(sys.argv[1])+'/'
main_file  = os.path.abspath(sys.argv[2])
max_num = int(sys.argv[3])
output_dir = os.path.abspath(sys.argv[4])+'/'

sentences = codecs.open(main_file,'r').read().strip().split('\n')
sampled_sentences = dict()

# sampling from the English side
added = 0
while added < 2 * max_num:
	i = random.randint(0,len(sentences)-1)
	if not sampled_sentences.has_key(sentences[i]) and len(sentences[i])>2:
		sampled_sentences[sentences[i]] = added
		added += 1

print len(sampled_sentences)

aligned_sentences = defaultdict(dict)
for root, dirs, files in os.walk(main_directory):
	for name in files:
		if name.endswith('.en'):
			for l in langs:
				if len(aligned_sentences[l])==0:
					aligned_sentences[l] = dict()
					fl = root + '/' + name[:-2]+l
					if os.path.exists(fl):
						print fl
						l_sentences = codecs.open(fl,'r').read().strip().split('\n')
						e_sentences = codecs.open(root + '/' +name,'r').read().strip().split('\n')

						for i in range(0,len(e_sentences)):
							if sampled_sentences.has_key(e_sentences[i]):
								aligned_sentences[l][sampled_sentences[e_sentences[i]]] = l_sentences[i]


final_sentences = defaultdict(list)
added = 0
for sen in sampled_sentences.keys():
	sen_id = sampled_sentences[sen]

	all_have = True
	for l in langs:
		if not aligned_sentences[l].has_key(sen_id):
			all_have = False
			break

	if all_have:
		final_sentences['en'].append(sen)
		for l in langs:
			final_sentences[l].append(aligned_sentences[l][sen_id])


langs.add('en')

for l in langs:
	final_sentences[l] = final_sentences[l][:max_num+1]


for l in langs:
	codecs.open(output_dir+l,'w').write('\n'.join(final_sentences[l]))


 
							

