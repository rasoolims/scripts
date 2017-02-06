import os,sys,codecs
from collections import defaultdict

print '[dict_file] [en_senti] [target_lang] [output]'
target_lang = sys.argv[3]
dic_reader = codecs.open(os.path.abspath(sys.argv[1]),'r')
trans = dict()
for line in dic_reader:
	spl = line.strip().split('\t')
	word,lang = spl[0],spl[1]
	if lang == target_lang:
		t = set()
		for i in range(2,len(spl)):
			t.add(spl[i].replace('_',' '))
		trans[word] = t

new_pos_senti_dict = defaultdict(list)
new_neg_senti_dict = defaultdict(list)

writer = codecs.open(os.path.abspath(sys.argv[4]),'w')
for line in codecs.open(os.path.abspath(sys.argv[2]),'r'):
	writer.write(line.strip()+'\n')
	word,pos,neg = line.strip().split()
	if word in trans:
		for t in trans[word]:
			new_pos_senti_dict[t].append(float(pos))
			new_neg_senti_dict[t].append(float(neg))

for t in new_pos_senti_dict.keys():
	if len(t.strip().split())==1:
		neg = float(sum(new_neg_senti_dict[t]))/len(new_neg_senti_dict[t])
		pos = float(sum(new_pos_senti_dict[t]))/len(new_pos_senti_dict[t])
		writer.write(t+'\t'+str(pos)+'\t'+str(neg)+'\n')

writer.close()