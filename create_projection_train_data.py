import os,sys,codecs
from collections import defaultdict
from termcolor import colored
from mst_dep_tree_loader import DependencyTree

if len(sys.argv)<5:
	print 'python create_projection_train_data.py [proj mst] [gold_target_sentences] [gold_src_mst] [intersection-file] [src_map_file] [dst_map_file] [output_file]'
	print 'two files do not need to be in the same size/order'
	sys.exit(0)

def is_punc(pos):
	return pos=="#" or pos=="$" or pos=="''" or pos=="(" or pos=="" or pos=="[" or pos=="]" or pos=="{" or pos=="}" or pos=="\"" or pos=="," or pos=="." or pos==":" or pos=="``" or pos=="-LRB-" or pos=="-RRB-" or pos=="-LSB-" or pos=="-RSB-" or pos=="-LCB-" or pos=="-RCB-"

def read_pos_map(path):
	pos_map=defaultdict(str)
	map_reader=open(path,'r')
	line=map_reader.readline()
	while line:
		split_line=line.strip().split('\t')
		if len(split_line)>1:
			pos_map[split_line[0]]=split_line[1]
		line=map_reader.readline()
	return pos_map

def extract_features(source_tree, dst_tree, src_head_index, src_mod_index, dst_head_index, dst_mod_index, label_set):
	features = list()
	source_head_pos = 'ROOT'
	src_head_dep = '_'
	if src_head_index>=0:
		source_head_pos = source_tree.tags[src_head_index]
		src_head_dep = source_tree.labels[src_head_index]
	features.append('source_head_pos:'+source_head_pos)
	features.append('src_head_dep:'+src_head_dep)

	source_mod_pos = source_tree.tags[src_mod_index]
	features.append('source_mod_pos:'+source_mod_pos)

	target_head_pos = 'ROOT'
	if dst_head_index>=0:
		target_head_pos = dst_tree.tags[dst_head_index]
	features.append('target_head_pos:'+target_head_pos)

	target_mod_pos = dst_tree.tags[dst_mod_index]
	features.append('target_mod_pos:'+target_mod_pos)

	dep_label = dst_tree.labels[dst_mod_index]
	features.append('dep_label:'+dep_label)

	features.append('src_distance:'+str(src_head_index-src_mod_index))
	features.append('dst_distance:'+str(dst_head_index-dst_mod_index))

	if src_head_index-src_mod_index>0 and dst_head_index-dst_mod_index<0:
		features.append('reverse_position')
	else:
		features.append('same_position')

	has_src_dep = dict()
	not_src_has_dep = dict()
	has_dst_dep = dict()
	not_dst_has_dep = dict()

	for l in label_set:
		has_src_dep[l] = '0'
		not_src_has_dep[l] = '1'
		has_dst_dep[l] = '0'
		not_dst_has_dep[l] = '1'


	for m in source_tree.reverse_tree[src_head_index+1]:
		l = source_tree.labels[m-1]
		not_src_has_dep[l] = '0'
		has_src_dep[l] = '1'

	for m in dst_tree.reverse_tree[dst_head_index+1]:
		l = dst_tree.labels[m-1]
		not_dst_has_dep[l] = '0'
		has_dst_dep[l] = '1'

	for l in label_set:
		if l == 'aux' or l == 'cop':
			if has_src_dep[l] == '1':
				features.append('has_src_dep:'+l)
			if not_src_has_dep[l]=='1':
				features.append('not_have_src_dep:'+l)
			if has_dst_dep[l]=='1':
				features.append('has_dst_dep:'+l)
			if not_dst_has_dep[l]=='1':
				features.append('not_have_dst_dep:'+l)

	# blows up feature space
	pair_features = list()
	for i in range(0,len(features)):
		for j in range(0, len(features)):
			if i!=j:
				pair_features.append('pair:'+features[i]+'|'+features[j])

	features+=pair_features
	return features

projected_trees=defaultdict(list)
line_count=0
reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
label_set = set()

cnt =0 
line=reader.readline()
while line:
	line=line.strip()
	if line:
		line_count+=1
		words=line.split('\t')
		tags=reader.readline().strip().split('\t')
		labels=reader.readline().strip().split('\t')
		for l in labels:
			label_set.add(l)
		hds=[int(x) for x in reader.readline().strip().split('\t')]
		sentence=' '.join(words)
		projected_trees[sentence].append([words,tags, labels,hds])
	cnt +=1
	if cnt%10000==0:
		sys.stdout.write(str(cnt)+'...')
	line=reader.readline()
sys.stdout.write(str(cnt)+'\n')
gold_trees=defaultdict()
gold_target_trees=defaultdict()
line_count=0
reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
reader2=codecs.open(os.path.abspath(sys.argv[3]),'r')
reader3=codecs.open(os.path.abspath(sys.argv[4]),'r')

src_pos_map=read_pos_map(os.path.abspath(sys.argv[5]))
dst_pos_map=read_pos_map(os.path.abspath(sys.argv[6]))

writer = codecs.open(os.path.abspath(sys.argv[7]),'w')

line=reader.readline()
line2=reader2.readline()
cnt =0 
while line:
	line=line.strip()
	line2=line2.strip()
	if line:
		line3=reader3.readline().strip()
		line_count+=1
		words=line.split('\t')
		words2=line2.split('\t')
		alignment=[-1]*len(words)
		
		try:
			spl=line3.split(' ')
			for x in spl:
				#print x
				spl2=x.split('-')
				s1=int(spl2[0])
				s2=int(spl2[1])
				if s2!=0:
					alignment[s2-1]=s1-1
		except:
			alignment=[-1]*len(words)

		tags2=reader2.readline().strip().split('\t')
		labels2=reader2.readline().strip().split('\t')
		hds2=[int(x) for x in reader2.readline().strip().split('\t')]

		tags = reader.readline().strip().split('\t')
		labels = reader.readline().strip().split('\t')
		hds = [int(x) for x in reader.readline().strip().split('\t')]

		sentence=' '.join(words)

		if not gold_trees.has_key(sentence):
			gold_trees[sentence]=[words2,tags2,labels2,hds2,alignment]
			gold_target_trees[sentence]=[labels,hds]

		cnt +=1
		if cnt%10000==0:
			sys.stdout.write(str(cnt)+'...')

	line=reader.readline()
	line=reader.readline()
	line2=reader2.readline()
	line2=reader2.readline()
sys.stdout.write(str(cnt)+'\n')
correct=0
all_dep=0
line_count=0

all_partial=0
partial_correct=0

local_percent=0.0
all_num=0
max_local_percent=0.0
min_local_percent=1.0
min_change=10000
max_change=0
avg_change=0.0
change_diag=defaultdict(int)

cnt = 0
for sentence_list in projected_trees.keys():
	for sentence in projected_trees[sentence_list]:
		proj_words = sentence[0]
		proj_tags = sentence[1]
		proj_labels = sentence[2]
		proj_heads = sentence[3]
		projected_tree = DependencyTree(proj_words,proj_tags,proj_heads,proj_labels)

		source_words = gold_trees[sentence_list][0]
		source_tags = gold_trees[sentence_list][1]
		source_labels = gold_trees[sentence_list][2]
		source_heads = gold_trees[sentence_list][3]
		alignment = gold_trees[sentence_list][4]
		source_tree = DependencyTree(source_words,source_tags,source_heads,source_labels)

		target_labels = gold_target_trees[sentence_list][0]
		target_heads = gold_target_trees[sentence_list][1]

		change_list = list()

		for i in range(0, len(proj_heads)):
			mod_aligned_index = alignment[i]
			head_aligned_index = alignment[proj_heads[i]-1]

			mod = i
			head = proj_heads[i]
			label = proj_labels[i]

			gold_head = target_heads[i]
			gold_label = target_labels[i]

			features = extract_features(source_tree, projected_tree, mod_aligned_index-1, head_aligned_index-1, head-1, mod,label_set)
			if gold_head == head and gold_label == label:
				writer.write('\t'.join(features)+'\taccept'+'\n')
			elif gold_head == head and gold_label!=label:
				writer.write('\t'.join(features)+'\tchange_label:'+gold_label+'\n')
			elif gold_head!=head:
				if target_heads[head-1]== mod +1:
					flip_children = True
					for dep in projected_tree.reverse_tree[head]:
						if dep != mod +1 and target_heads[dep-1] != mod + 1:
							flip_children = False
							break

					# flip head and child
					if gold_label==label:
						if flip_children:
							writer.write('\t'.join(features)+'\tflip_head_child_and_all_children'+'\n')
						else:
							writer.write('\t'.join(features)+'\tflip_head_child'+'\n')
					elif gold_label!=label:
						if flip_children:
							writer.write('\t'.join(features)+'\tflip_head_child_and_all_children'+'_change_label:'+gold_label+'\n')
						else:
							writer.write('\t'.join(features)+'\tflip_head_child_change_label:'+gold_label+'\n')
					else:
						writer.write('\t'.join(features)+'\treject'+'\n')

		cnt += 1
		if cnt %1000 ==0:
			sys.stdout.write(str(cnt)+'...')

sys.stdout.write(str(cnt)+'\n')
writer.close()

print 'done!'