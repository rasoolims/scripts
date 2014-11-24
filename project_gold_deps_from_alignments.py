import os,sys,math,operator,codecs,traceback
from collections import defaultdict

if len(sys.argv)<5:
	print 'python project_gold_deps_from_alignments.py [src_mst_file] [dst_mst_file] [align_intersection_file] [output_file_name] [keep_full(bool)] '
	print 'by looking at dst trees, just keeps the ones that are preserved in the alignment in dst trees'
	sys.exit(0)

src_mst_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
dst_mst_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
align_reader=codecs.open(os.path.abspath(sys.argv[3]),'r')
output_file_name=os.path.abspath(sys.argv[4])
keep_full=True if sys.argv[5]=='true' else False

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
src_dst_no_restriction_writer=codecs.open(output_file_name,'w')

# getting src projections
sys.stdout.write('getting src projections...')
sys.stdout.flush()

alldeps=0
preserved_deps=0
for s in src_alignment_dic.keys():
	if s%10000==0:
		sys.stdout.write(str(s)+'...')
		sys.stdout.flush()
	src_tree=src_trees[s]
	dst_tree=dst_trees[s]
	alignment=src_alignment_dic[s]

	no_restriction_heads=list()
	no_restriction_labels=list()
	proj_no_restriction_heads=list()
	proj_no_restriction_labels=list()

	exception=False

	is_full=True
	for mod in range(0,len(dst_tree[0])):
		no_restriction_heads.append('-1')
		no_restriction_labels.append("_")
		proj_no_restriction_heads.append('-1')
		proj_no_restriction_labels.append("_")
		if dst_tree[3][mod]=='-1' or dst_tree[3][mod]==-1:
			is_full=False

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
				dst_mod_pos=dst_tree[1][dst_mod-1]
				dst_mod_word=dst_tree[0][dst_mod-1]
				dst_head_pos='ROOT'
				dst_head_word='ROOT'
				if dst_head>0:
					dst_head_pos=dst_tree[1][dst_head-1]
					dst_head_word=dst_tree[0][dst_head-1]
				mod_pair=src_word+'\t'+dst_mod_word
				head_pair=src_head_word+'\t'+dst_head_word
				alldeps+=1

				proj_no_restriction_heads[dst_mod-1]=str(dst_head)
				proj_no_restriction_labels[dst_mod-1]=src_label

				if dst_tree[3][dst_mod-1]==dst_head or (is_full and keep_full):
					no_restriction_heads[dst_mod-1]=str(dst_head)
					no_restriction_labels[dst_mod-1]=src_label
					preserved_deps+=1
			except:
				print src_tree[1]
				print ' '.join(dst_tree[0])
				print len(dst_tree[0]),len(dst_tree[1]),len(dst_tree[3]),src_head,src_mod,dst_head,dst_mod
				print alignment
				print s
				exception=True
				print traceback.format_exc()
				#sys.exit(0)

	# still keeping full trees regardless of its validity
	all_dep=True
	for h in proj_no_restriction_heads:
		if h==-1 or h=='-1':
			all_dep=False
			break
	if all_dep:
		no_restriction_labels=proj_no_restriction_labels
		no_restriction_heads=proj_no_restriction_heads


	# no restriction output
	if not exception:
		src_dst_no_restriction_writer.write('\t'.join(dst_tree[0])+'\n')
		src_dst_no_restriction_writer.write('\t'.join(dst_tree[1])+'\n')
		src_dst_no_restriction_writer.write('\t'.join(no_restriction_labels)+'\n')
		src_dst_no_restriction_writer.write('\t'.join(no_restriction_heads)+'\n\n')
	else:
		src_dst_no_restriction_writer.write('\t'.join(dst_tree[0])+'\n')
		src_dst_no_restriction_writer.write('\t'.join(dst_tree[1])+'\n')
		src_dst_no_restriction_writer.write('\t'.join(['_']*len(dst_tree[0]))+'\n')
		src_dst_no_restriction_writer.write('\t'.join(['-1']*len(dst_tree[0]))+'\n\n')

src_dst_no_restriction_writer.flush()
src_dst_no_restriction_writer.close()

sys.stdout.write('\nalldeps: '+str(alldeps)+' preserved_deps: '+str(preserved_deps))
sys.stdout.write('\n')
