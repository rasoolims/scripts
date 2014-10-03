import os,sys,math,operator,codecs,traceback
from collections import defaultdict

if len(sys.argv)<7:
	print 'python project_alignment.py [src_mst_file] [dst_mst_file] [align_file] [pmi_file] [output_file_name] [max_number_of_members]'
	sys.exit(0)


src_mst_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
dst_mst_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
align_reader=codecs.open(os.path.abspath(sys.argv[3]),'r')
pmi_reader=codecs.open(os.path.abspath(sys.argv[4]),'r')
output_file_name=os.path.abspath(sys.argv[5])
pmi_threshold=int(sys.argv[6])


# initializing the data structs
pmi_dict=defaultdict(float)
pmi2_dict=defaultdict(float)
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

# reading pmi and pmi^2
sys.stdout.write('reading pmis...')
sys.stdout.flush()
line=pmi_reader.readline()
while line:
	line=line.strip()
	if line:
		flds=line.split('\t')
		pair=flds[0]+'\t'+flds[1]
		pmi_dict[pair]=float(flds[4])
		pmi2_dict[pair]=float(flds[5])
		prob_dict[pair]=flds
	line=pmi_reader.readline()

sys.stdout.write('\n')
sys.stdout.write('sorting pmis...')
sys.stdout.flush()
sorted_pmis=sorted(pmi_dict.iteritems(), key=operator.itemgetter(1))[0:pmi_threshold]
sorted_pmi2s=sorted(pmi2_dict.iteritems(), key=operator.itemgetter(1))[0:pmi_threshold]

pmi_list=set()
pmi2_list=set()
for p in sorted_pmis:
	pmi_list.add(p[0])
for p in sorted_pmi2s:
	pmi2_list.add(p[0])


sys.stdout.write('len of pmi_list: '+str(len(pmi_list))+'\n')


# initializing different types of outputs
src_dst_no_restriction_writer=codecs.open(output_file_name+'.src_dst_no_restriction','w')
src_dst_pos_restriction_writer=codecs.open(output_file_name+'.src_dst_pos_restriction','w')
src_dst_pmi_restriction_writer=codecs.open(output_file_name+'.src_dst_pmi_restriction','w')
src_dst_pmi2_restriction_writer=codecs.open(output_file_name+'.src_dst_pmi2_restriction','w')
src_dst_pos_pmi_restriction_writer=codecs.open(output_file_name+'.src_dst_pos_pmi_restriction','w')
src_dst_pos_pmi2_restriction_writer=codecs.open(output_file_name+'.src_dst_pos_pmi2_restriction','w')
src_dst_pos_pmi_1_2_restriction_writer=codecs.open(output_file_name+'.src_dst_pos_pmi_1_2_restriction','w')

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

	pmi_restriction_heads=list()
	pmi_restriction_labels=list()
	pmi_restriction_projection=False

	pmi2_restriction_heads=list()
	pmi2_restriction_labels=list()
	pmi2_restriction_projection=False

	exception=False

	for mod in range(0,len(dst_tree[0])):
		no_restriction_heads.append('-1')
		no_restriction_labels.append("_")
		no_restriction_confidence.append(1.0)
		pos_restriction_heads.append('-1')
		pos_restriction_labels.append("_")
		pmi_restriction_heads.append('-1')
		pmi_restriction_labels.append("_")
		pmi2_restriction_heads.append('-1')
		pmi2_restriction_labels.append("_")

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
			
			
			#print src_tree[1]
			#print ' '.join(dst_tree[0])
			#print len(dst_tree[1]),src_head,src_mod,dst_head,dst_mod
			#print alignment
			#print s
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
				confidence=math.exp(pmi2_dict[mod_pair]+pmi2_dict[head_pair])
				no_restriction_heads[dst_mod-1]=str(dst_head)#+':'+str(confidence)





				# pos restriction
				if src_pos==dst_mod_pos and src_head_pos==dst_head_pos:
					pos_restriction_heads[dst_mod-1]=str(dst_head)
					pos_restriction_labels[dst_mod-1]=src_label
					pos_restriction_projection=True


					# pmi restriction
					if head_pair in pmi_list and mod_pair in pmi_list:
						pmi_restriction_heads[dst_mod-1]=str(dst_head)
						pmi_restriction_labels[dst_mod-1]=src_label
						pmi_restriction_projection=True					

					if head_pair in pmi2_list and mod_pair in pmi2_list:
						pmi2_restriction_heads[dst_mod-1]=str(dst_head)
						pmi2_restriction_labels[dst_mod-1]=src_label
						pmi2_restriction_projection=True		

			except:
				print src_tree[1]
				print ' '.join(dst_tree[0])
				print len(dst_tree[1]),src_head,src_mod,dst_head,dst_mod
				print alignment
				print s
				exception=True
				print traceback.format_exc()
				#sys.exit(0)

	# no restriction output
	if no_restriction_projection and not exception:
		src_dst_no_restriction_writer.write('\t'.join(dst_tree[0])+'\n')
		src_dst_no_restriction_writer.write('\t'.join(dst_tree[1])+'\n')
		src_dst_no_restriction_writer.write('\t'.join(no_restriction_labels)+'\n')
		src_dst_no_restriction_writer.write('\t'.join(no_restriction_heads)+'\n\n')
	if pos_restriction_projection and not exception:
		src_dst_pos_restriction_writer.write('\t'.join(dst_tree[0])+'\n')
		src_dst_pos_restriction_writer.write('\t'.join(dst_tree[1])+'\n')
		src_dst_pos_restriction_writer.write('\t'.join(pos_restriction_labels)+'\n')
		src_dst_pos_restriction_writer.write('\t'.join(pos_restriction_heads)+'\n\n')
	if pmi_restriction_projection and not exception:
		src_dst_pmi_restriction_writer.write('\t'.join(dst_tree[0])+'\n')
		src_dst_pmi_restriction_writer.write('\t'.join(dst_tree[1])+'\n')
		src_dst_pmi_restriction_writer.write('\t'.join(pmi_restriction_labels)+'\n')
		src_dst_pmi_restriction_writer.write('\t'.join(pmi_restriction_heads)+'\n\n')
	if pmi2_restriction_projection and not exception:
		src_dst_pmi2_restriction_writer.write('\t'.join(dst_tree[0])+'\n')
		src_dst_pmi2_restriction_writer.write('\t'.join(dst_tree[1])+'\n')
		src_dst_pmi2_restriction_writer.write('\t'.join(pmi2_restriction_labels)+'\n')
		src_dst_pmi2_restriction_writer.write('\t'.join(pmi2_restriction_heads)+'\n\n')


src_dst_no_restriction_writer.flush()
src_dst_no_restriction_writer.close()
src_dst_pos_restriction_writer.flush()
src_dst_pos_restriction_writer.close()
src_dst_pmi_restriction_writer.flush()
src_dst_pmi_restriction_writer.close()
src_dst_pmi2_restriction_writer.flush()
src_dst_pmi2_restriction_writer.close()

sys.stdout.write('\n')



dst_src_no_restriction_writer=codecs.open(output_file_name+'.dst_src_no_restriction','w')
dst_src_pos_restriction_writer=codecs.open(output_file_name+'.dst_src_pos_restriction','w')
dst_src_pmi_restriction_writer=codecs.open(output_file_name+'.dst_src_pmi_restriction','w')
dst_src_pmi2_restriction_writer=codecs.open(output_file_name+'.dst_src_pmi2_restriction','w')
dst_src_pos_pmi_restriction_writer=codecs.open(output_file_name+'.dst_src_pos_pmi_restriction','w')
dst_src_pos_pmi2_restriction_writer=codecs.open(output_file_name+'.dst_src_pos_pmi2_restriction','w')
dst_src_pos_pmi_1_2_restriction_writer=codecs.open(output_file_name+'.dst_src_pos_pmi_1_2_restriction','w')



