import os,sys,math,operator,codecs,traceback
from collections import defaultdict


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

def same_pos_kind(p1,p2):
	if p1==p2:
		return True

	if p1=='PRON':
		if p2=='DET' or p2=='NOUN' or p2=='ADJ':
			return True
	if p1=='NOUN':
		if p2=='DET' or p2=='PRON':
			return True
	if p1=='DET':
		if p2=='NOUN' or p2=='PRON' or p2=='NUM':
			return True;
	if p1=='PRT':
		if p2=='ADV':
			return True
	if p1=='ADV':
		if p2=='PRT' or p2=='ADJ':
			return True
	if p1=='ADJ':
		if p2=='ADV' or p2=='PRON':
			return True
	if p1=='X':
		if p2=='NUM' or p2=='.':
			return True
	if p1=='.':
		if p2=='X':
			return True
	if p1=='NUM':
		if p2=='X' or p2=='DET':
			return True

	return False


if len(sys.argv)<4:
	print 'python project_tree_tag_with_alignment.py [src_mst_file] [dst_raw_file] [align_intersection_file] [src_pos_map] [output_file_name]'
	sys.exit(0)

src_mst_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
dst_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
align_reader=codecs.open(os.path.abspath(sys.argv[3]),'r')
output_file_name=os.path.abspath(sys.argv[5])
src_pos_map=read_pos_map(os.path.abspath(sys.argv[4]))
prob_dict=defaultdict()

src_alignment_dic=defaultdict()
dst_alignment_dic=defaultdict()
src_trees=defaultdict()
dst_words=defaultdict()


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
line=dst_reader.readline()
sys.stdout.write('reading target file...')
sys.stdout.flush()

line_count=0
while line:
	line=line.strip()
	if line:
		line_count+=1
		words=line.split(' ')

		dst_words[line_count]=words
		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')
			sys.stdout.flush()
	line=dst_reader.readline()
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
src_dst_no_restriction_writer=codecs.open(output_file_name,'w')

# getting src projections
sys.stdout.write('getting src projections...')
sys.stdout.flush()

for s in src_alignment_dic.keys():
	if s%10000==0:
		sys.stdout.write(str(s)+'...')
		sys.stdout.flush()
	src_tree=src_trees[s]
	dst_word=dst_words[s]
	dst_pos=['***']*len(dst_word)
	alignment=src_alignment_dic[s]

	no_restriction_heads=list()
	no_restriction_labels=list()
	no_restriction_projection=False


	exception=False

	for mod in range(0,len(dst_word)):
		no_restriction_heads.append('-1')
		no_restriction_labels.append("_")

	for mod in range(0,len(src_tree[0])):
		src_head=src_tree[3][mod]
		src_mod=mod+1
		src_pos=src_tree[1][mod]
		src_word=src_tree[0][mod]
		src_label=src_tree[2][mod]

		src_head_pos='***'
		src_head_word='***'
		if src_head>0:
			src_head_pos=src_tree[1][src_head-1]
			src_head_word=src_tree[0][src_head-1]

		if alignment.has_key(src_mod):
			sp=src_pos
			if src_pos_map.has_key(src_pos):
				sp=src_pos_map[src_pos]
			dst_mod=alignment[src_mod]	
			if dst_mod>0:
				dst_pos[dst_mod-1]=sp
		if alignment.has_key(src_head):
			shp=src_head_pos
			if src_pos_map.has_key(src_head_pos):
				shp=src_pos_map[src_head_pos]

			dst_head=alignment[src_head]
			if dst_head>0:
				dst_pos[dst_head-1]=shp

		if alignment.has_key(src_mod) and alignment.has_key(src_head):
			dst_head=alignment[src_head]
			dst_mod=alignment[src_mod]	
			
			try:
				# no restriction
				no_restriction_labels[dst_mod-1]=src_label
				no_restriction_projection=True
				dst_mod_word=dst_word[dst_mod-1]
				dst_head_pos='***'
				dst_head_word='***'
				if dst_head>0:
					dst_head_word=dst_word[dst_head-1]
				dst_mod_pos='***'
				no_restriction_heads[dst_mod-1]=str(dst_head)#+':'+str(confidence)

				# pos restriction
				sp=src_pos
				if src_pos_map.has_key(src_pos):
					sp=src_pos_map[src_pos]
				shp=src_head_pos
				if src_pos_map.has_key(src_head_pos):
					shp=src_pos_map[src_head_pos]

				if dst_mod>0:
					dst_pos[dst_mod-1]=sp
				if dst_head>0:
					dst_pos[dst_head-1]=shp

			except:
				print src_tree[1]
				print ' '.join(dst_word)
				print len(dst_word),src_head,src_mod,dst_head,dst_mod
				print alignment
				print s
				exception=True
				print traceback.format_exc()
				#sys.exit(0)

	# no restriction output
	if not exception:
		#for i in range(0,len(no_restriction_heads)):
			#if no_restriction_heads[i]=='-1':
				#dst_pos[i]='***'
		src_dst_no_restriction_writer.write('\t'.join(dst_word)+'\n')
		src_dst_no_restriction_writer.write('\t'.join(dst_pos)+'\n')
		src_dst_no_restriction_writer.write('\t'.join(no_restriction_labels)+'\n')
		src_dst_no_restriction_writer.write('\t'.join(no_restriction_heads)+'\n\n')
	else:
		src_dst_no_restriction_writer.write('\t'.join(dst_word)+'\n')
		src_dst_no_restriction_writer.write('\t'.join(['***']*len(dst_word))+'\n')
		src_dst_no_restriction_writer.write('\t'.join(['_']*len(dst_word))+'\n')
		src_dst_no_restriction_writer.write('\t'.join(['-1']*len(dst_word))+'\n\n')


src_dst_no_restriction_writer.flush()
src_dst_no_restriction_writer.close()
sys.stdout.write('\n')
