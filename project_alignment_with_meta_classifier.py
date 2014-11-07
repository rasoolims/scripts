import os,sys,math,operator,codecs,traceback
from collections import defaultdict
from avg_perceptron import avg_perceptron

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

if len(sys.argv)<8:
	print 'python project_alignment_with_meta_classifier.py [learning_model_file] [src_mst_file] [dst_mst_file] [align_intersection_file] [src_pos_map] [dst_pos_map] [output_file_name] [is_labeled]'
	sys.exit(0)

classfier=avg_perceptron(os.path.abspath(sys.argv[1]))
classfier.labels=set(['0','1'])

src_mst_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
dst_mst_reader=codecs.open(os.path.abspath(sys.argv[3]),'r')
align_reader=codecs.open(os.path.abspath(sys.argv[4]),'r')

src_pos_map=read_pos_map(os.path.abspath(sys.argv[5]))
dst_pos_map=read_pos_map(os.path.abspath(sys.argv[6]))


output_file_name=os.path.abspath(sys.argv[7])

labeled=False
if len(sys.argv)>8 and sys.argv[8]=='labeled':
	labeled=True

prob_dict=defaultdict()

src_alignment_dic=defaultdict()
dst_alignment_dic=defaultdict()
src_trees=defaultdict()
dst_trees=defaultdict()


# reading source tree files
sys.stdout.write('reading source tree files...')
sys.stdout.flush()

line=src_mst_reader.readline()
line_count=0
while line:
	line=line.strip()
	if line:
		line_count+=1
		words=line.split('\t')
		tags=src_mst_reader.readline().strip().split('\t')
		for t in range(0,len(tags)):
			if src_pos_map.has_key(tags[t]):
				tags[t]=src_pos_map[tags[t]]

		labels=src_mst_reader.readline().strip().split('\t')
		hds=src_mst_reader.readline().strip().split('\t')
		heads=list()
		for h in hds:
			heads.append(int(round(float(h))))

		src_trees[line_count]=words,tags,labels,heads
		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')
			sys.stdout.flush()
	line=src_mst_reader.readline()


sys.stdout.write('\n')

# reading target tree files
line=dst_mst_reader.readline()
sys.stdout.write('reading target tree files...')
sys.stdout.flush()

line_count=0
while line:
	line=line.strip()
	if line:
		line_count+=1
		words=line.split('\t')
		tl=dst_mst_reader.readline().strip()
		tags=tl.split('\t')
		main_tags=tl.split('\t')
		for t in range(0,len(tags)):
			if dst_pos_map.has_key(tags[t]):
				tags[t]=dst_pos_map[tags[t]]

		labels=dst_mst_reader.readline().strip().split('\t')
		hds=dst_mst_reader.readline().strip().split('\t')
		heads=list()
		for h in hds:
			heads.append(-1)

		dst_trees[line_count]=words,tags,labels,heads,main_tags
		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')
			sys.stdout.flush()
	line=dst_mst_reader.readline()
sys.stdout.write('\n')

# reading line by line alignments
line_count=0
sys.stdout.write('reading alignments...')
sys.stdout.flush()
line=align_reader.readline()
while line:
	line=line.strip()
	if line:
		line_count+=1
		src_alignment_dic[line_count]=defaultdict()
		dst_alignment_dic[line_count]=defaultdict()

		flds=line.split(' ')
		for fld in flds:
			split_flds=fld.split('-')
			src_index=int(split_flds[0])
			dst_index=int(split_flds[1])
			src_alignment_dic[line_count][src_index]=dst_index
			dst_alignment_dic[line_count][dst_index]=src_index
		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')
			sys.stdout.flush()
	line=align_reader.readline()
sys.stdout.write('\n')


# initializing different types of outputs
writer=codecs.open(output_file_name,'w')

# getting src projections
sys.stdout.write('getting src projections...')
sys.stdout.flush()

for s in src_alignment_dic.keys():
	if s%10000==0:
		sys.stdout.write(str(s)+'...')
		sys.stdout.flush()
	src_tree=src_trees[s]
	dst_tree=dst_trees[s]
	alignment=src_alignment_dic[s]

	no_restriction_heads=list()
	no_restriction_labels=list()

	for mod in range(0,len(dst_tree[0])):
		no_restriction_heads.append('-1')
		no_restriction_labels.append("_")

	align_dic=dict()
	for mod in range(0,len(src_tree[0])):
		src_head=src_tree[3][mod]
		src_mod=mod+1
		src_pos=src_tree[1][mod]
		src_word=src_tree[0][mod]
		src_label=src_tree[2][mod]

		src_head_pos='ROOT'
		src_head_word='ROOT'
		if src_head>0:
			src_head_pos=src_tree[1][src_head-1]
			src_head_word=src_tree[0][src_head-1]

		if alignment.has_key(src_mod) and alignment.has_key(src_head):
			instance_lst=list()
			dst_head=alignment[src_head]
			dst_mod=alignment[src_mod]
			
			src_distance=abs(src_mod-src_head)
			if src_distance>10:
				src_distance=10
			elif src_distance>5:
				src_distance=5
			instance_lst.append('sd:'+str(src_distance))

			dst_distance=abs(dst_mod-dst_head)
			if dst_distance>10:
				dst_distance=10
			elif dst_distance>5:
				dst_distance=5
			instance_lst.append('dd:'+str(dst_distance))

			mod_distance=abs(src_mod-dst_mod)
			if mod_distance>10:
				mod_distance=10
			elif mod_distance>5:
				mod_distance=5
			instance_lst.append('md:'+str(mod_distance))

			head_distance=abs(src_head-dst_head)
			if head_distance>10:
				head_distance=10
			elif head_distance>5:
				head_distance=5
			instance_lst.append('hd:'+str(head_distance))

			src_direction='l'
			dst_direction='l'
			if src_head<src_mod:
				src_direction='r'
			if dst_head<dst_mod:
				dst_direction='r'
			instance_lst.append('sdr:'+src_direction)
			instance_lst.append('ddr:'+dst_direction)
			instance_lst.append('sd_dr:'+src_direction+'|'+dst_direction)

			instance_lst.append('l:'+src_label)
			
			try:
				# no restriction
				dst_mod_pos=dst_tree[1][dst_mod-1]
				dst_mod_word=dst_tree[0][dst_mod-1]

				lab='0'
				if (not labeled or src_label==dst_tree[2][dst_mod-1]) and dst_tree[3][dst_mod-1]==dst_head:
					lab='1'

				dst_head_pos='ROOT'
				dst_head_word='ROOT'
				if dst_head>0:
					dst_head_pos=dst_tree[1][dst_head-1]
					dst_head_word=dst_tree[0][dst_head-1]

				instance_lst.append('dmp:'+dst_mod_pos)
				instance_lst.append('dsp:'+dst_head_pos)
				instance_lst.append('dmhp:'+dst_mod_pos+'|'+dst_head_pos)
				instance_lst.append('dmpsmp:'+dst_mod_pos+'|'+src_pos)
				instance_lst.append('dmpshp:'+dst_mod_pos+'|'+src_head_pos)
				instance_lst.append('dhpsmp:'+dst_head_pos+'|'+src_pos)
				instance_lst.append('dhpshp:'+dst_head_pos+'|'+src_head_pos)

				instance_lst.append('dmpsmw:'+dst_mod_pos+'|'+src_word)
				instance_lst.append('dmpshw:'+dst_mod_pos+'|'+src_head_word)
				instance_lst.append('dhpsmw:'+dst_head_pos+'|'+src_word)
				instance_lst.append('dhpshw:'+dst_head_pos+'|'+src_head_word)

				instance_lst.append('dmpsd:'+dst_mod_pos+'|'+str(dst_distance)+'|'+src_direction)
				instance_lst.append('dspsd:'+dst_head_pos+'|'+str(dst_distance)+'|'+src_direction)
				instance_lst.append('dmhpdd:'+dst_mod_pos+'|'+dst_head_pos+'|'+str(dst_distance)+'|'+src_direction)
				instance_lst.append('dmpsmp_sd:'+dst_mod_pos+'|'+src_pos+'|'+str(dst_distance)+'|'+src_direction)
				instance_lst.append('dmpshp_sd:'+dst_mod_pos+'|'+src_head_pos+'|'+str(dst_distance)+'|'+src_direction)
				instance_lst.append('dhpsmp_sd:'+dst_head_pos+'|'+src_pos+'|'+str(dst_distance)+'|'+src_direction)
				instance_lst.append('dhpshp_sd:'+dst_head_pos+'|'+src_head_pos+'|'+str(dst_distance)+'|'+src_direction)

				instance_lst.append('dmhpdd:'+dst_mod_pos+'|'+dst_head_pos+'|'+str(dst_distance)+'|'+dst_direction)
				instance_lst.append('dmpsmp_dd:'+dst_mod_pos+'|'+src_pos+'|'+str(dst_distance)+'|'+dst_direction)
				instance_lst.append('dmpshp_dd:'+dst_mod_pos+'|'+src_head_pos+'|'+str(dst_distance)+'|'+dst_direction)
				instance_lst.append('dhpsmp_dd:'+dst_head_pos+'|'+src_pos+'|'+str(dst_distance)+'|'+dst_direction)
				instance_lst.append('dhpshp_dd:'+dst_head_pos+'|'+src_head_pos+'|'+str(dst_distance)+'|'+dst_direction)
				
				instance_lst.append('smp:'+src_pos)
				instance_lst.append('shp:'+src_head_pos)
				instance_lst.append('smhpl:'+src_pos+'|'+src_head_pos+'|'+src_label)
				instance_lst.append('smhp:'+src_pos+'|'+src_head_pos)
				instance_lst.append('smpl:'+src_pos+'|'+src_label)
				instance_lst.append('shpl:'+src_head_pos+'|'+src_label)

				instance_lst.append('smwp:'+src_word+'|'+src_pos)
				instance_lst.append('smhwp:'+src_word+'|'+src_head_pos)
				instance_lst.append('smww:'+src_word+'|'+src_head_word)

				instance_lst.append('shwp:'+src_head_word+'|'+src_pos)
				instance_lst.append('smhwp:'+src_head_word+'|'+src_head_pos)

				same_mod_pos='f'
				if src_pos==dst_mod_pos:
					same_mod_pos='t'
				instance_lst.append('s_mp:'+same_mod_pos)

				same_head_pos='f'
				if src_head_pos==dst_head_pos:
					same_head_pos='t'
				instance_lst.append('s_hp:'+same_head_pos)

				both_same_pos='f'
				if same_mod_pos and same_head_pos:
					both_same_pos='t'
				instance_lst.append('bsp:'+both_same_pos)

				dst_len=len(dst_tree[1])
				#instance_lst.append('dl:'+str(dst_len))

				len_diff=dst_len-len(src_tree[1])
				if len_diff>10:
					len_diff=10
				elif len_diff>5:
					len_diff=5
				instance_lst.append('ld:'+str(len_diff))

				align_dic[dst_mod-1]=instance_lst

				no_restriction_heads[dst_mod-1]=str(dst_head)
				no_restriction_labels[dst_mod-1]=src_label
			except:
				print src_tree[1]
				print ' '.join(dst_tree[0])
				print len(dst_tree[0]),len(dst_tree[1]),len(dst_tree[3]),src_head,src_mod,dst_head,dst_mod
				print alignment
				print s
				exception=True
				print traceback.format_exc()

	tree_len=len(align_dic)
	proportion=int(round(float((10*float(tree_len)/(len(dst_tree[0])-1))%10)))

	max_len=0
	i=1
	ln=0
	is_full=True
	while i<len(no_restriction_heads):
		if no_restriction_heads[i]=='-1':
			is_full=False
			if ln>max_len:
				max_len=ln
			ln=0
		else:
			ln+=1
		i+=1

	if ln>max_len:
		max_len=ln


	fin_feats=dict()
	if max_len>=0 or proportion>=0:
		for mod in align_dic.keys():
			has_left='t'
			has_right='t'

			if mod>1:
				if no_restriction_heads[mod-1]=='-1':
					has_left='f'
			if mod<len(no_restriction_heads)-1:
				if no_restriction_heads[mod+1]=='-1':
					has_right='f'
			align_dic[mod].insert(0,'hl:'+has_left)
			align_dic[mod].insert(0,'hr:'+has_right)
			align_dic[mod].insert(0,'pr:'+str(proportion))

			instance_lst=list()
			for i in range(0,len(align_dic[mod])):
				instance_lst.append(align_dic[mod][i].replace(':','|'))
			fin_feats[mod]=instance_lst
	for i in range(0,len(dst_tree[0])):
		#if not fin_feats.has_key(i):
			#print 'no for '+str(i)
		if is_full:
			dst_tree[3][i]=str(no_restriction_heads[i])
			dst_tree[2][i]=no_restriction_labels[i]
		elif not fin_feats.has_key(i) or classfier.argmax(fin_feats[i],True)=='0':
			dst_tree[3][i]='-1'
			dst_tree[2][i]='_'
			#print 'classfier is not ok with '+str(i)
		else:
			dst_tree[3][i]=str(no_restriction_heads[i])
			dst_tree[2][i]=no_restriction_labels[i]
			#print 'classfier is ok with '+str(i)

	writer.write('\t'.join(dst_tree[0])+'\n')
	writer.write('\t'.join(dst_tree[4])+'\n')
	writer.write('\t'.join(dst_tree[2])+'\n')
	writer.write('\t'.join(dst_tree[3])+'\n\n')

	#sys.exit(0)

writer.flush()
writer.close()
sys.stdout.write('\n')
