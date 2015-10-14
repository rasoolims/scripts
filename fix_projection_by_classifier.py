import os,sys,codecs
from collections import defaultdict
from termcolor import colored
from mst_dep_tree_loader import DependencyTree
from avg_perceptron import avg_perceptron


if len(sys.argv)<10:
	print 'python fix_projection_by_classifier.py [proj mst] [gold_target_sentences] [gold_src_mst] [intersection-file] [src_map_file] [dst_map_file] [trained_model] [iter#] [output_file]'
	print 'two files do not need to be in the same size/order'
	sys.exit(0)

def is_punc(pos):
	return pos=="#" or pos=="$" or pos=="''" or pos=="(" or pos=="" or pos=="[" or pos=="]" or pos=="{" or pos=="}" or pos=="\"" or pos=="," or pos=="." or pos==":" or pos=="``" or pos=="-LRB-" or pos=="-RRB-" or pos=="-LSB-" or pos=="-RSB-" or pos=="-LCB-" or pos=="-RCB-"

def trav(rev_head,h,visited):
	if rev_head.has_key(h):
		for d in rev_head[h]:
			if d in visited:
				return True
			visited.append(d)
			trav(rev_head,d,visited)
	return False

def is_full(heads):
	for dep1 in range(1,len(heads)+1):
		head1=heads[dep1-1]
		if head1<0:
			return False
	return True

def is_projective(heads):
	rev_head=defaultdict(list)
	for dep1 in range(1,len(heads)+1):
		head1=heads[dep1-1]
		if head1>=0:
			rev_head[head1].append(dep1)

	visited=list()
	#print rev_head
	if trav(rev_head,0,visited):
		return False
	if len(visited)<len(heads) and is_full(heads):
		return False

	rootN=0
	for dep1 in range(1,len(heads)+1):
		head1=heads[dep1-1]

		if rev_head.has_key(dep1):
			for d2 in rev_head[dep1]:
				if (d2<head1 and head1<dep1) or (d2>head1 and head1>dep1) and head1>0:
					return False

		if head1==0:
			rootN+=1
		for dep2 in range(1,len(heads)+1):
			head2=heads[dep2-1]
			if head1==-1 or head2==-1:
				continue
			if dep1>head1 and head1!=head2:
				if dep1>head2 and dep1<dep2 and head1<head2:
					return False
				if dep1<head2 and dep1>dep2 and head1<dep2:
					return False
			if dep1<head1 and head1!=head2:
				if head1>head2 and head1<dep2 and dep1<head2:
					return False
				if head1<head2 and head1>dep2 and dep1<dep2:
					return False
	if rootN!=1:
		return False
	return True

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
model_path  = os.path.abspath(sys.argv[7])
iter_num = int(sys.argv[8])
dap=avg_perceptron(model_path+'.model_'+str(iter_num),model_path+'.lab')

writer = codecs.open(os.path.abspath(sys.argv[9]),'w')

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


		change_list = list()

		predictions = dict()

		for i in range(0, len(proj_heads)):
			if proj_heads[i]==-1:
				continue
			mod_aligned_index = alignment[i]
			head_aligned_index = alignment[proj_heads[i]-1]
			mod = i
			head = proj_heads[i]
			label = proj_labels[i]
			features = extract_features(source_tree, projected_tree, mod_aligned_index-1, head_aligned_index-1, head-1, mod,label_set)
			argmax=dap.argmax(features,True)
			if argmax != 'accept':
				predictions[mod]= argmax

		done_with_flip_children = False
		done_with_flip = False
		done_with_change_label = False

		actions = list()
		while len(predictions)>0:
			if not done_with_flip_children:
				for p in predictions.keys():
					if not p in predictions:
						continue
					if predictions[p].startswith('flip_head_child_and_all_children'):
						head = proj_heads[p]
						actions.append('flip_head_child_and_all_children:'+str(p)+':'+str(head))
						projected_tree.heads[p] = projected_tree.heads[head-1]
						projected_tree.heads[head-1] = p + 1
						projected_tree.reverse_tree[head].remove(p+1)
						if head in projected_tree.reverse_tree[projected_tree.heads[p]]:
							projected_tree.reverse_tree[projected_tree.heads[p]].remove(head)
						projected_tree.reverse_tree[projected_tree.heads[p]].add(p+1)
						projected_tree.reverse_tree[p+1].add(head)
						deps = set(projected_tree.reverse_tree[head])
						for dep in deps:
							projected_tree.heads[dep-1] = p+1
							projected_tree.reverse_tree[head].remove(dep)
							projected_tree.reverse_tree[p+1].add(dep)
							if dep-1  in predictions:
								del predictions[dep-1]
						if predictions[p].startswith('flip_head_child_and_all_children_change_label'):
							projected_tree.labels[p] = predictions[p][predictions[p].rfind(':')+1:]
						del predictions[p]

						if not is_projective(projected_tree.heads):
							print 'flip_head_child_and_all_children_change_label',p,head
							print projected_tree.tree_str()
							sys.exit(0)
				done_with_flip_children = True
			elif not done_with_flip:
				has_flip = False
				for p in predictions.keys():
					if not p in predictions:
						continue
					if predictions[p].startswith('flip_head_child'):
						head = proj_heads[p]
						actions.append('flip_head_child:'+str(p)+':'+str(head))
						projected_tree.heads[p] = projected_tree.heads[head-1]
						projected_tree.heads[head-1] = p+1
						if head in projected_tree.reverse_tree[projected_tree.heads[p]]:
							projected_tree.reverse_tree[projected_tree.heads[p]].remove(head)
						projected_tree.reverse_tree[projected_tree.heads[p]].add(p+1)
						projected_tree.reverse_tree[head].remove(p+1)
						projected_tree.reverse_tree[p+1].add(head)
						del predictions[p]
						if not is_projective(projected_tree.heads):
							deps = set(projected_tree.reverse_tree[head])
							for dep in deps:
								if (dep > head and p+1 <dep) or (dep<head and p+1 >dep):
									projected_tree.heads[dep-1] = p+1
									projected_tree.reverse_tree[head].remove(dep)
									projected_tree.reverse_tree[p+1].add(dep)
									if dep-1  in predictions:
										del predictions[dep-1]
						
							if not is_projective(projected_tree.heads):
								print 'flip_head_child',p,head
								print projected_tree.reverse_tree
								print projected_tree.tree_str()

								sys.exit(0)
				done_with_flip = True
			elif not done_with_change_label:
				for p in predictions.keys():
					if not p in predictions:
						continue					
					if predictions[p].startswith('change_label:'):
						projected_tree.labels[p] = predictions[p][predictions[p].rfind(':')+1:]
						del predictions[p]
				done_with_change_label = True
			else:
				for p in predictions.keys():
					if not p in predictions:
						continue				

					if predictions[p]=='reject':
						projected_tree.heads[p]=-1
						projected_tree.labels[p]='_'
					del predictions[p]


		writer.write(projected_tree.tree_str()+'\n\n')
		cnt += 1
		if cnt %100 ==0:
			sys.stdout.write(str(cnt)+'...')

sys.stdout.write(str(cnt)+'\n')
writer.close()

print 'done!'

