import os,sys

prop_conllu = open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')
syntax_conllu = open(os.path.abspath(sys.argv[2]),'r').read().strip().split('\n\n')
writer = open(os.path.abspath(sys.argv[3]),'w')

syntax_sen_dic = dict()
for sen in syntax_conllu:
	sentence = sen.strip().split('\n')[1]
	sentence = sentence[sentence.find('=')+1:].strip()
	syntax_sen_dic[sentence] = sen

for sen in prop_conllu:
	sentence = sen.strip().split('\n')[0]
	sentence = sentence[sentence.find(':')+1:].strip()
	if sentence in syntax_sen_dic:
		writer.write(syntax_sen_dic[sentence]+'\n\n')
	else:
		print(sentence)
		sys.exit(1)
writer.close()