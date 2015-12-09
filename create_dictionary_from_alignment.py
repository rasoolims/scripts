import os,sys,math,operator,codecs,traceback
from collections import defaultdict


if len(sys.argv)<5:
	print 'python create_dictionary_from_alignment.py [src_raw_file] [dst_raw_file] [align_intersection_file] [output_file_name]'
	sys.exit(0)

src_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
dst_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
align_reader=codecs.open(os.path.abspath(sys.argv[3]),'r')
output_file_name=os.path.abspath(sys.argv[4])
prob_dict=defaultdict()

src_alignment_dic=defaultdict()
dst_alignment_dic=defaultdict()
src_sentences=defaultdict()
dst_sentences=defaultdict()


# reading source tree files
sys.stdout.write('reading source tree files...')
sys.stdout.flush()

line=src_reader.readline()
line_count=0
while line:
	line=line.strip()
	if line:
		line_count+=1
		src_sentences[line_count]=line.split(' ')
		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')
			sys.stdout.flush()
	line=src_reader.readline()


sys.stdout.write('\n')

# reading target tree files
line=dst_reader.readline()
sys.stdout.write('reading target tree files...')
sys.stdout.flush()

line_count=0
while line:
	line=line.strip()
	if line:
		line_count+=1
		dst_sentences[line_count]=line.split(' ')
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
src_dst_no_restriction_writer=codecs.open(output_file_name+'.src_dst_no_restriction','w')
src_dst_pos_restriction_writer=codecs.open(output_file_name+'.src_dst_pos_restriction','w')
src_dst_pos_restriction_writer2=codecs.open(output_file_name+'.src_dst_or_pos_restriction','w')

# getting src projections
sys.stdout.write('getting src projections...')
sys.stdout.flush()

alignment_dict = defaultdict()

for s in src_alignment_dic.keys():
	if s%100000==0:
		sys.stdout.write(str(s)+'...')
		sys.stdout.flush()
	src_sentence=src_sentences[s]
	dst_setence=dst_sentences[s]
	alignment=src_alignment_dic[s]

	for i in range(1,len(src_sentence)+1):
		if alignment.has_key(i):
			if not alignment_dict.has_key(src_sentence[i-1]):
				alignment_dict[src_sentence[i-1]] = defaultdict(int)
			alignment_dict[src_sentence[i-1]][dst_setence[alignment[i]-1]]+=1

writer = codecs.open(output_file_name,'w')
for word in alignment_dict.keys():
	sorted_x = sorted(alignment_dict[word].items(), key=operator.itemgetter(1),reverse=True)
	writer.write(word+'\t'+sorted_x[0][0]+'\n')
writer.close()

sys.stdout.write('\n')
