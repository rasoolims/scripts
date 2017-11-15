import os,sys,codecs

pos_dict = {'HYPH':'PUNCT','NIL':'PUNCT','PRF':'ADJ','!':'PUNCT' , '#':'PUNCT' , '$':'PUNCT' , '\'\'':'PUNCT' , '(':'PUNCT' , ')':'PUNCT' , ',':'PUNCT' , '-LRB-':'PUNCT' , '-RRB-':'PUNCT' , '.':'PUNCT' , ':':'PUNCT' , '?':'PUNCT' , 'CC':'CONJ' , 'CD':'NUM' , 'CD|RB':'X' , 'DT':'DET' , 'EX':'DET' , 'FW':'X' , 'IN':'ADP' , 'IN|RP':'ADP' , 'JJ':'ADJ' , 'JJR':'ADJ' , 'JJRJR':'ADJ' , 'JJS':'ADJ' , 'JJ|RB':'ADJ' , 'JJ|VBG':'ADJ' , 'LS':'X' , 'MD':'VERB' , 'NN':'NOUN' , 'NNP':'NOUN' , 'NNPS':'NOUN' , 'NNS':'NOUN' , 'NN|NNS':'NOUN' , 'NN|SYM':'NOUN' , 'NN|VBG':'NOUN' , 'NP':'NOUN' , 'PDT':'DET' , 'POS':'PRT' , 'PRP':'PRON' , 'PRP$':'PRON' , 'PRP|VBP':'PRON' , 'PRT':'PRT' , 'RB':'ADV' , 'RBR':'ADV' , 'RBS':'ADV' , 'RB|RP':'ADV' , 'RB|VBG':'ADV' , 'RN':'X' , 'RP':'PRT' , 'SYM':'X' , 'TO':'PRT' , 'UH':'X' , 'VB':'VERB' , 'VBD':'VERB' , 'VBD|VBN':'VERB' , 'VBG':'VERB' , 'VBG|NN':'VERB' , 'VBN':'VERB' , 'VBP':'VERB' , 'VBP|TO':'VERB' , 'VBZ':'VERB' , 'VP':'VERB' , 'WDT':'DET' , 'WH':'X' , 'WP':'PRON' , 'WP$':'PRON' , 'WRB':'ADV' , '``':'PUNCT'}
sens = codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')

for sen in sens:
	lines = sen.strip().split('\n')
	writer.write('#sen_id\n')
	for line in lines:
		spl = line.strip().split('\t')
		new_spl = spl[0:3] + [pos_dict[spl[4]]] + spl[5:7] + [spl[8]]+[spl[10]] + ['_','_']
		writer.write('\t'.join(new_spl)+'\n')
	writer.write('\n')
writer.close()


