from mst_dep_tree_loader import DependencyTree
import sys, codecs, os

conll2tag = os.path.dirname(os.path.abspath(sys.argv[0]))+'/conll2tag.py'

use_in_word = True
arg_ = sys.argv[1:]
writer = codecs.open(arg_[1],'w')
intersects = []
for line in open(arg_[3], 'r'):
	intsct = dict()
	for spl in line.split():
		si,ti= spl.strip().split('-')
		si,ti = int(si), int(ti)
		if si!=0:
			intsct[si] = ti
	intersects.append(intsct)
target_trees = DependencyTree.load_trees_from_conll_file(arg_[4])

rec = codecs.open(arg_[5],'r').read().strip().split('\n')
dictionaries = dict()
for r in rec:
	spl = r.split('\t')
	dictionaries[spl[0]] = spl[1]


reader = codecs.open(arg_[0], 'r')
line = reader.readline()
sent_num = 0
while line:
	spl = line.strip().split('\t')
	if len(spl)>6:
		word_num = int(spl[0])
		l_id = spl[5]
		spl[1] = spl[1].lower()
		if word_num in intersects[sent_num]:
			target_word = target_trees[sent_num].words[intersects[sent_num][word_num]-1].lower()
			spl[2] = spl[1]
			spl[1] = target_word
		elif dictionaries.has_key(spl[1]):
			if not use_in_word:
				spl[2] = spl[1]
				spl[1] = dictionaries[spl[1]]
			else:
				spl[2] = spl[1]
				spl[1] = dictionaries[spl[1]]
		elif spl[3]=='PUNCT' or spl[3]=='.':
			spl[2] = spl[1]
		else:
			if not use_in_word:
				spl[2] = spl[1]
				spl[1] = spl[1]
			else:
				spl[2] = spl[1]
	else:
		sent_num+=1

	writer.write('\t'.join(spl)+'\n')
	line = reader.readline()
command = 'python -u ' + conll2tag + ' ' + arg_[1] + ' '+ arg_[2] +' &'
print command
os.system(command)