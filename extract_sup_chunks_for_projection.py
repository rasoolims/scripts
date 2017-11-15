import os,sys,codecs

sup_res = set(codecs.open(os.path.abspath(sys.argv[1]),'r',encoding='utf-8').read().strip().split('\n\n'))
proj_res = codecs.open(os.path.abspath(sys.argv[2]),'r',encoding='utf-8').read().strip().split('\n\n')

sup_dict = dict()
for res in sup_res:
	spl = res.strip().split('\n')
	sen_words = []
	for s in spl:
		sen_words.append(s.split()[0])

	sup_dict[' '.join(sen_words)] = res.strip()


writer = codecs.open(os.path.abspath(sys.argv[3]),'w',encoding='utf-8')
for res in proj_res:
	spl = res.strip().split('\n')
	sen_words = []
	for s in spl:
		sen_words.append(s.split()[0])
	sentence = ' '.join(sen_words)

	writer.write(sup_dict[sentence]+'\n\n')
writer.close()