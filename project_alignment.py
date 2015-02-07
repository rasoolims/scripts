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


if len(sys.argv)<5:
	print 'python project_alignment.py [src_mst_file] [dst_mst_file] [align_intersection_file] [src_pos_map] [dst_pos_map] [output_file_name]'
	sys.exit(0)

src_mst_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
dst_mst_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
align_reader=codecs.open(os.path.abspath(sys.argv[3]),'r')
output_file_name=os.path.abspath(sys.argv[6])
src_pos_map=read_pos_map(os.path.abspath(sys.argv[4]))
dst_pos_map=read_pos_map(os.path.abspath(sys.argv[5]))
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
		tags=dst_mst_reader.readline().strip().split('\t')
		labels=dst_mst_reader.readline().strip().split('\t')
		hds=dst_mst_reader.readline().strip().split('\t')
		heads=list()
		for h in hds:
			heads.append(int(round(float(h))))

		dst_trees[line_count]=words,tags,labels,heads
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
src_dst_no_restriction_writer=codecs.open(output_file_name+'.src_dst_no_restriction','w')
src_dst_pos_restriction_writer=codecs.open(output_file_name+'.src_dst_pos_restriction','w')
src_dst_pos_restriction_writer2=codecs.open(output_file_name+'.src_dst_or_pos_restriction','w')

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
	no_restriction_confidence=list()
	no_restriction_projection=False

	pos_restriction_heads=list()
	pos_restriction_labels=list()
	pos_restriction_heads2=list()
	pos_restriction_labels2=list()
	pos_restriction_projection=False

	exception=False

	for mod in range(0,len(dst_tree[0])):
		no_restriction_heads.append('-1')
		no_restriction_labels.append("_")
		no_restriction_confidence.append(1.0)
		pos_restriction_heads.append('-1')
		pos_restriction_labels.append("_")
		pos_restriction_heads2.append('-1')
		pos_restriction_labels2.append("_")

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
			dst_head=alignment[src_head]
			dst_mod=alignment[src_mod]	
			
			try:
				# no restriction
				no_restriction_labels[dst_mod-1]=src_label
				no_restriction_projection=True
				dst_mod_pos=dst_tree[1][dst_mod-1]
				dst_mod_word=dst_tree[0][dst_mod-1]
				dst_head_pos='ROOT'
				dst_head_word='ROOT'
				if dst_head>0:
					dst_head_pos=dst_tree[1][dst_head-1]
					dst_head_word=dst_tree[0][dst_head-1]
				mod_pair=src_word+'\t'+dst_mod_word
				head_pair=src_head_word+'\t'+dst_head_word
				no_restriction_heads[dst_mod-1]=str(dst_head)#+':'+str(confidence)

				# pos restriction
				sp=src_pos
				if src_pos_map.has_key(src_pos):
					sp=src_pos_map[src_pos]
				dp=dst_mod_pos
				if dst_pos_map.has_key(dst_mod_pos):
					dp=dst_pos_map[dst_mod_pos]
				shp=src_head_pos
				if src_pos_map.has_key(src_head_pos):
					shp=src_pos_map[src_head_pos]
				dhp=dst_head_pos
				if dst_pos_map.has_key(dst_head_pos):
					dhp=dst_pos_map[dst_head_pos]

				if sp==dp and shp==dhp:
					pos_restriction_heads[dst_mod-1]=str(dst_head)
					pos_restriction_labels[dst_mod-1]=src_label
					pos_restriction_projection=True
				
				if (same_pos_kind(sp,dp) and  same_pos_kind(shp,dhp)) or dst_mod_word==src_word:
					pos_restriction_heads2[dst_mod-1]=str(dst_head)
					pos_restriction_labels2[dst_mod-1]=src_label
					pos_restriction_projection=True
			except:
				print src_tree[1]
				print ' '.join(dst_tree[0])
				print len(dst_tree[0]),len(dst_tree[1]),len(dst_tree[3]),src_head,src_mod,dst_head,dst_mod
				print alignment
				print s
				exception=True
				print traceback.format_exc()
				#sys.exit(0)

	# no restriction output
	if not exception:
		src_dst_no_restriction_writer.write('\t'.join(dst_tree[0])+'\n')
		src_dst_no_restriction_writer.write('\t'.join(dst_tree[1])+'\n')
		src_dst_no_restriction_writer.write('\t'.join(no_restriction_labels)+'\n')
		src_dst_no_restriction_writer.write('\t'.join(no_restriction_heads)+'\n\n')

		src_dst_pos_restriction_writer.write('\t'.join(dst_tree[0])+'\n')
		src_dst_pos_restriction_writer.write('\t'.join(dst_tree[1])+'\n')
		src_dst_pos_restriction_writer.write('\t'.join(pos_restriction_labels)+'\n')
		src_dst_pos_restriction_writer.write('\t'.join(pos_restriction_heads)+'\n\n')

		src_dst_pos_restriction_writer2.write('\t'.join(dst_tree[0])+'\n')
		src_dst_pos_restriction_writer2.write('\t'.join(dst_tree[1])+'\n')
		src_dst_pos_restriction_writer2.write('\t'.join(pos_restriction_labels2)+'\n')
		src_dst_pos_restriction_writer2.write('\t'.join(pos_restriction_heads2)+'\n\n')
	else:
		src_dst_no_restriction_writer.write('\t'.join(dst_tree[0])+'\n')
		src_dst_no_restriction_writer.write('\t'.join(dst_tree[1])+'\n')
		src_dst_no_restriction_writer.write('\t'.join(['_']*len(dst_tree[0]))+'\n')
		src_dst_no_restriction_writer.write('\t'.join(['-1']*len(dst_tree[0]))+'\n\n')

		src_dst_pos_restriction_writer.write('\t'.join(dst_tree[0])+'\n')
		src_dst_pos_restriction_writer.write('\t'.join(dst_tree[1])+'\n')
		src_dst_pos_restriction_writer.write('\t'.join(['_']*len(dst_tree[0]))+'\n')
		src_dst_pos_restriction_writer.write('\t'.join(['-1']*len(dst_tree[0]))+'\n\n')

		src_dst_pos_restriction_writer2.write('\t'.join(dst_tree[0])+'\n')
		src_dst_pos_restriction_writer2.write('\t'.join(dst_tree[1])+'\n')
		src_dst_pos_restriction_writer2.write('\t'.join(['_']*len(dst_tree[0]))+'\n')
		src_dst_pos_restriction_writer2.write('\t'.join(['-1']*len(dst_tree[0]))+'\n\n')


src_dst_no_restriction_writer.flush()
src_dst_no_restriction_writer.close()
src_dst_pos_restriction_writer.flush()
src_dst_pos_restriction_writer.close()
src_dst_pos_restriction_writer2.flush()
src_dst_pos_restriction_writer2.close()
sys.stdout.write('\n')
