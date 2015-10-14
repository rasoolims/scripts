#! /usr/bin/python

import codecs, os, random, sys, operator
from collections import defaultdict
from extract_dependency_spans import SpanInfo, SpanDicts
from mst_dep_tree_loader import DependencyTree
from random import randrange
import kenlm

def get_simple_lm(file_path):
	prob_dic = defaultdict(float)
	probs_lines = codecs.open(file_path,'r').read().split('\n')
	for pl in probs_lines:
		spl = pl.strip().split('\t')
		if len(spl)<2:
			continue
		trigram = spl[0]
		prob = float(spl[1])
		prob_dic[trigram] = prob
	return prob_dic

def get_pos_lm_score(prob_dic,tags):
	new_tags = ['<START>','<START>']+tags + ['<END>']
	score = 0
	for i in range(2,len(new_tags)):
		trigram = new_tags[i-2]+' '+new_tags[i-1]+' '+new_tags[i] 
		if prob_dic.has_key(trigram):
			score+=prob_dic[trigram]
		else:
			return float('inf')
	return score

if __name__ == '__main__':
	if len(sys.argv)<5:
		print 'args: [input mst_full_tree_file] [kenlm_model file] [simple pos lm file] [input span_file] [expanded_trees_file]'
		sys.exit(0)
	full_trees = DependencyTree.load_trees_from_file(os.path.abspath(sys.argv[1]))
	print len(full_trees)
	lang_model = kenlm.LanguageModel(os.path.abspath(sys.argv[2]))
	simple_lm = get_simple_lm(os.path.abspath(sys.argv[3]))
	span_dict = SpanDicts.load_from_file(os.path.abspath(sys.argv[4]))
	print len(span_dict.head_word_info)
	print len(span_dict.span_info_dic)

	generated_tree_dict = defaultdict(float)

	writer = codecs.open(os.path.abspath(sys.argv[5]),'w',encoding = 'utf-8')
	mst_writer = codecs.open(os.path.abspath(sys.argv[5])+'.mst','w',encoding = 'utf-8')

	cnt = 0
	for tree in full_trees:
		if len(tree.words)<4:
			continue
		#writer.write(' '.join(tree.words)+'\n')
		#writer.write(' '.join([str(x) for x in tree.heads])+'\n')
		generated_tree_dict = defaultdict(float)
		for random_index in range(0,len(tree.words)):
			#writer.write(str(random_index)+'\n')

			# put phrase after that word regarding prev/next pos
			prev_pos = '' if random_index==0 else tree.tags[random_index-1]
			next_pos = '' if random_index== len(tree.words)-1 else  tree.tags[random_index+1]
			context = prev_pos+' '+next_pos

			#writer.write('\n###put phrase after that word regarding prev/next pos\n\n')
			cand_list = span_dict.context_pos_info[context]
			if len(cand_list)>0:
				for i in range(0,min(100,len(cand_list))):
					random_selction = span_dict.span_info_dic[cand_list[randrange(0,len(cand_list))]]
					new_tree = 	tree.expand_tree(random_selction,random_index)
					sen = ' '.join(new_tree.words)
					if generated_tree_dict.has_key(sen):
						continue
					tag_score = get_pos_lm_score(simple_lm,new_tree.tags)
					
					if tag_score ==float('inf'):
						continue
					score = lang_model.score(sen.lower()) + tag_score
					generated_tree_dict[sen] = (score/len(new_tree.words) ,new_tree, 'phrase after that word regarding prev/next pos',random_index)
					#writer.write(' '.join(new_tree.words)+'\n'+str(score)+'\n')
					#writer.write(' '.join([str(x) for x in new_tree.heads])+'\n')

			# extend that phrase for the word being head with the same dependency
			head_word = tree.words[random_index]
			head_dep = tree.labels[random_index]
			context = head_word+' '+head_dep

			#writer.write('\n###extend that phrase for the word being head with the same dependency\n\n')

			cand_list = span_dict.head_word_dep_info[context]
			if len(cand_list)>0:
				for i in range(0,min(100,len(cand_list))):
					random_selction = span_dict.span_info_dic[cand_list[randrange(0,len(cand_list))]]
					new_tree = 	tree.extend_tree_inclusive(random_selction,random_index)
					sen = ' '.join(new_tree.words)
					if generated_tree_dict.has_key(sen):
						continue
					tag_score = get_pos_lm_score(simple_lm,new_tree.tags)
					if tag_score ==float('inf'):
						continue
					score = lang_model.score(' '.join(new_tree.words).lower()) + tag_score
					generated_tree_dict[' '.join(new_tree.words).lower()] = (score/len(new_tree.words) ,new_tree, 'same_dependency',random_index)
					#writer.write(' '.join(new_tree.words)+'\n'+str(score)+'\n')
					#writer.write(' '.join([str(x) for x in new_tree.heads])+'\n')

			# extend the phrase for that word (head_pos the same)
			head_word = tree.tags[random_index]

			#writer.write('\n###extend the phrase for that word (head_pos the same)\n\n')
			cand_list = span_dict.head_of_head_pos_info[head_word]
			if len(cand_list)>0:
				for i in range(0,min(100,len(cand_list))):
					random_selction = span_dict.span_info_dic[cand_list[randrange(0,len(cand_list))]]
					new_tree = 	tree.expand_tree(random_selction,random_index)
					sen = ' '.join(new_tree.words)
					if generated_tree_dict.has_key(sen):
						continue
					tag_score = get_pos_lm_score(simple_lm,new_tree.tags)
					if tag_score ==float('inf'):
						continue
					score = lang_model.score(' '.join(new_tree.words).lower()) + tag_score
					generated_tree_dict[' '.join(new_tree.words).lower()] = (score/len(new_tree.words) ,new_tree,'extend the phrase for that word (head_pos the same)',random_index)
					#writer.write(' '.join(new_tree.words)+'\n'+str(score)+'\n')
					#writer.write(' '.join([str(x) for x in new_tree.heads])+'\n')


		#writer.write('\n*********************************************\n\n')
		cnt+=1
		if cnt%1 == 0:
			sys.stdout.write('%s\r' % (str(cnt)+'...'))

		sorted_x = sorted(generated_tree_dict.items(), key=operator.itemgetter(1), reverse=True)
		writer.write(' '.join(tree.words)+'\n')
		for i in range(0,min(len(sorted_x), 10)):
			new_tree = sorted_x[i][1][1]
			kind = sorted_x[i][1][2]
			score = sorted_x[i][1][0]
			if score < -3:
				break
			random_index = sorted_x[i][1][3]
			if (i+1)%100 ==0:
				sys.stdout.write('%s\r' % (str(i+1)+'...'))
			writer.write(' '.join(new_tree.words)+'\n'+str(score)+' : '+kind+' : '+str(random_index)+'\n')
			writer.write(' '.join([str(x) for x in new_tree.heads])+'\n')
			tree_list = list()
			tree_list.append('\t'.join(new_tree.words))
			tree_list.append('\t'.join(new_tree.tags))
			tree_list.append('\t'.join(new_tree.labels))
			hds=list()
			for h in new_tree.heads:
				hds.append(str(h))
			tree_list.append('\t'.join(hds))
			mst_writer.write('\n'.join(tree_list)+'\n\n')
		writer.write('\n*********************************************\n\n')
	writer.close()

	#test_main()