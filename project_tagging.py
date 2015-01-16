import os,sys,math,operator,codecs,traceback
from collections import defaultdict

if len(sys.argv)<5:
	print 'python project_tagging.py [src_tag_file] [dst_tag_file] [align_intersection_file] [output_file_name]'
	sys.exit(0)

src_tag_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
dst_tag_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
align_reader=codecs.open(os.path.abspath(sys.argv[3]),'r')
output_file_name=os.path.abspath(sys.argv[4])

prob_dict=defaultdict()

src_alignment_dic=defaultdict()
dst_alignment_dic=defaultdict()
src_tags=defaultdict()
dst_words=defaultdict()


# reading source tag files
sys.stdout.write('reading source tag files...')
sys.stdout.flush()

line=src_tag_reader.readline()
line_count=0
while line:
	line=line.strip()
	if line:
		line_count+=1
		flds=line.split(' ')
		words=list()
		for f in flds:
			spl=f.strip().split('_')
			if len(spl)==2:
				words.append(spl[1])
		src_tags[line_count]=words
	line=src_tag_reader.readline()


sys.stdout.write('\n')

# reading target tag files
sys.stdout.write('reading target tag files...')
sys.stdout.flush()

line=dst_tag_reader.readline()
line_count=0
while line:
	line=line.strip()
	if line:
		line_count+=1
		flds=line.split(' ')
		words=list()
		for f in flds:
			spl=f.strip().split('_')
			if len(spl)==2:
				words.append(spl[0])
		dst_words[line_count]=words
	line=dst_tag_reader.readline()

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


writer=codecs.open(output_file_name,'w')

# getting projections
sys.stdout.write('getting projections...')
sys.stdout.flush()

for s in src_alignment_dic.keys():
	if s%10000==0:
		sys.stdout.write(str(s)+'...')
		sys.stdout.flush()
	src_tag=src_tags[s]
	dst_w=dst_words[s]
	alignment=src_alignment_dic[s]

	dst_tags=list()

	for m in range(0,len(dst_w)):
		dst_tags.append('***')

	for m in range(0,len(src_tag)):
		t=src_tag[m]
		if alignment.has_key(m):
			dst_tags[alignment[m]]=t


	output=list()
	for i in range(0,len(dst_w)):
		output.append(dst_w[i]+'_'+dst_tags[i])
	writer.write(' '.join(output)+'\n')

writer.flush()
writer.close()
sys.stdout.write('\n')
