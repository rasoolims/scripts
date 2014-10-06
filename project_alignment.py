import os,sys,math,operator,codecs,traceback
from collections import defaultdict

if len(sys.argv)<5:
	print 'python project_alignment.py [src_mst_file] [dst_mst_file] [align_intersection_file] [output_file_name]'
	sys.exit(0)

src_mst_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
dst_mst_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
align_reader=codecs.open(os.path.abspath(sys.argv[3]),'r')
output_file_name=os.path.abspath(sys.argv[4])

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
	pos_restriction_projection=False

	exception=False

	for mod in range(0,len(dst_tree[0])):
		no_restriction_heads.append('-1')
		no_restriction_labels.append("_")
		no_restriction_confidence.append(1.0)
		pos_restriction_heads.append('-1')
		pos_restriction_labels.append("_")

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
				if src_pos==dst_mod_pos and src_head_pos==dst_head_pos:
					pos_restriction_heads[dst_mod-1]=str(dst_head)
					pos_restriction_labels[dst_mod-1]=src_label
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
	else:
		src_dst_no_restriction_writer.write('\t'.join(dst_tree[0])+'\n')
		src_dst_no_restriction_writer.write('\t'.join(dst_tree[1])+'\n')
		src_dst_no_restriction_writer.write('\t'.join(['_']*len(dst_tree[0]))+'\n')
		src_dst_no_restriction_writer.write('\t'.join(['-1']*len(dst_tree[0]))+'\n\n')
		src_dst_pos_restriction_writer.write('\t'.join(dst_tree[0])+'\n')
		src_dst_pos_restriction_writer.write('\t'.join(dst_tree[1])+'\n')
		src_dst_pos_restriction_writer.write('\t'.join(['_']*len(dst_tree[0]))+'\n')
		src_dst_pos_restriction_writer.write('\t'.join(['-1']*len(dst_tree[0]))+'\n\n')	

src_dst_no_restriction_writer.flush()
src_dst_no_restriction_writer.close()
src_dst_pos_restriction_writer.flush()
src_dst_pos_restriction_writer.close()

sys.stdout.write('\n')

dst_src_no_restriction_writer=codecs.open(output_file_name+'.dst_src_no_restriction','w')
dst_src_pos_restriction_writer=codecs.open(output_file_name+'.dst_src_pos_restriction','w')