import os,sys,math
from collections import defaultdict

def read_ngram_counts(file_path):
	lines = open(file_path,'r').read().strip().split('\n')
	four_gram_count = defaultdict(int)
	five_gram_count = defaultdict(int)
	trigram_count = defaultdict(int)
	bigram_count = defaultdict(int)
	ngram_prob = defaultdict(float)


	for line in lines:
		spl = ('<start> <start> '+line+' <end>').split(' ')
		for i in range(2, len(spl)):
			trigram_count[spl[i-2]+' '+spl[i-1]+' '+spl[i]]+=1
			bigram_count[spl[i-2]+' '+spl[i-1]]+=1

			if i < len(spl) -1:
				four_gram_count[spl[i-2]+' '+spl[i-1]+' '+spl[i] + ' '+ spl[i+1]]+=1
				if  i < len(spl) -2:
					five_gram_count[spl[i-2]+' '+spl[i-1]+' '+spl[i] + ' '+ spl[i+1] + ' '+ spl[i+2]]+=1

	for trigram in trigram_count.keys():
		bigram = trigram.split(' ')[0]+' '+ trigram.split(' ')[1]
		ngram_prob[trigram] = float(trigram_count[trigram])/bigram_count[bigram]
	'''
	for fourgram in four_gram_count.keys():
		trigram = fourgram.split(' ')[0]+' '+ fourgram.split(' ')[1]+' '+ fourgram.split(' ')[2]
		ngram_prob[fourgram] = float(four_gram_count[fourgram])/trigram_count[trigram]

	for fivegram in five_gram_count.keys():
		fourgram = fivegram.split(' ')[0]+' '+ fivegram.split(' ')[1]+' '+ fivegram.split(' ')[2]+' '+ fivegram.split(' ')[3]
		ngram_prob[fivegram] = float(five_gram_count[fivegram])/four_gram_count[fourgram]
	'''
	return ngram_prob


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


print cosine_similarity(read_ngram_counts(os.path.abspath(sys.argv[1])),read_ngram_counts(os.path.abspath(sys.argv[2])))