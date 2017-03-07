import os,sys,math
from collections import defaultdict

def read_ngram_counts(file_path):
	lines = open(file_path,'r').read().strip().split('\n')
	trigram_count = defaultdict(int)
	ngram_prob = defaultdict(float)

	possibles_tags = set()
	for line in lines:
		spl = ('<start> <start> '+line+' <end>').split(' ')
		for i in range(2, len(spl)):
			trigram_count[spl[i-2]+' '+spl[i-1]+' '+spl[i]]+=1
			possibles_tags.add(spl[i-2])
			possibles_tags.add(spl[i-1])
			possibles_tags.add(spl[i])

	possible_trigrams = math.pow(len(possibles_tags),3)
	all_count = possible_trigrams*0.5
	for trigram in trigram_count.keys():
		all_count+= trigram_count[trigram]

	for trigram in trigram_count.keys():
		ngram_prob[trigram] = (trigram_count[trigram]+0.5) / all_count

	return ngram_prob


def kl(f1, f2):
	div = 0
	for t in f2.keys():
		f = 0.5 if f1[t]==0 else f1[t]
		try:
			div+= f2[t]*math.log(f2[t]/f)
		except:
			div = div

	return math.pow(1.0/div,2)

def cosine_similarity(dic1, dic2):
	nom = 0.0
	denom1 = 0.0
	denom2 = 0.0
	for element in dic1.keys():
		nom += dic1[element]*dic2[element]
		denom1+= dic1[element]*dic1[element]

	for element in dic2.keys():
		denom2+= dic2[element]*dic2[element]

	return nom /(math.sqrt(denom1)*math.sqrt(denom2))


input_folder = os.path.abspath(sys.argv[1])+'/'
writer = open(os.path.abspath(sys.argv[2]),'w')
for f1 in os.listdir(input_folder):
	for f2 in os.listdir(input_folder):
		if f1 < f2:
			print f1,f2
			n1 = read_ngram_counts(input_folder+f1)
			n2 = read_ngram_counts(input_folder+f2)
			kl1 = kl(n1, n2)
			kl2 = kl(n2, n1)
			cos_sim = cosine_similarity(n1, n2)
			writer.write(f1+'\t'+f2+'\t'+str(cos_sim)+'\t'+str(kl1)+'\n')
			writer.write(f2+'\t'+f1+'\t'+str(cos_sim)+'\t'+str(kl2)+'\n')

writer.close()