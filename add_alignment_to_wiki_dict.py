# coding: utf-8
import os,sys,codecs,random
from collections import defaultdict

if len(sys.argv)<4:
	print 'wiki_dict alignment_dict target_lang output_file'
	sys.exit(0)

target_lang = sys.argv[3] 
dic_reader = codecs.open(os.path.abspath(sys.argv[1]),'r')
trans = defaultdict(set)
for line in dic_reader:
	spl = line.strip().split('\t')
	word,lang = spl[0],spl[1]
	if lang == target_lang:
		t = set()
		for i in range(2,len(spl)):
			t.add(spl[i].replace('_',' '))
		trans[word] = t
other_dict = {line.strip().split()[0]:line.strip().split()[1] for line in codecs.open(os.path.abspath(sys.argv[2]),'r')}

for word in other_dict.keys():
	trans[word].add(other_dict[word])

writer = codecs.open(os.path.abspath(sys.argv[4]),'w')
for word in trans.keys():
	translations = trans[word]
	writer.write(word+'\t'+target_lang+'\t'+'\t'.join(translations)+'\n')

writer.close()
