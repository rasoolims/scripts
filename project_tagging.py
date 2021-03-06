import os,sys,math,operator,codecs,traceback
from collections import defaultdict

if len(sys.argv)<5:
	print 'python project_tagging.py [src_tag_file] [dst_tag_file] [align_intersection_file] [tag_mapping_file] [wiki_file(null if nothing)] [output_file_name] [hard assignment(optional)]'
	sys.exit(0)

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

def read_wiktionary_map(path):
	pos_map=defaultdict(str)
	map_reader=open(path,'r')
	line=map_reader.readline()
	while line:
		split_line=line.strip().split('\t')
		if len(split_line)==2:
			word=split_line[0].lower()
			tag=split_line[1]
			if not pos_map.has_key(word):
				pos_map[word]=set()
			pos_map[word].add(tag)

		line=map_reader.readline()
	return pos_map

src_tag_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
dst_tag_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
align_reader=codecs.open(os.path.abspath(sys.argv[3]),'r')
pos_map=read_pos_map(os.path.abspath(sys.argv[4]))

wiki_map=dict()
if sys.argv[5]!='null':
	wiki_map=read_wiktionary_map(os.path.abspath(sys.argv[5]))

print len(wiki_map)
output_file_name=os.path.abspath(sys.argv[6])

hard_assignment=False
if len(sys.argv)>7 and sys.argv[7]=='hard':
	hard_assignment=True
	print 'hard assignment'
 

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
			x=f.strip().rfind('_')
			if x>0:
				tag=f.strip()[x+1:]
				if pos_map.has_key(tag):
					tag=pos_map[tag]
				#elif pos_map.has_key(tag[:tag.find('-')]):
					#tag=pos_map[tag[:tag.find('-')]]
				else:
					print tag,' does not exist'
				words.append(tag)
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
			x=f.strip().rfind('_')
			if x>0:
				word=f.strip()[:x]
				words.append(word)
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

	try:
		for m in range(0,len(src_tag)):
			t=src_tag[m]
			if alignment.has_key(m+1):
				w=dst_w[alignment[m+1]-1].lower()

				if (wiki_map.has_key(w) and t in wiki_map[w]) or (not wiki_map.has_key(w) and not hard_assignment) or (not wiki_map.has_key(w)): # and not (t=='PRT'  or t=='ADV' or t=='ADJ' or t=='NOUN' or t=='.')
					#if t!='PRT':
					dst_tags[alignment[m+1]-1]=t

		output=list()

		is_full=True
		for i in range(0,len(dst_w)):
			if dst_tags[i]=='***':
				is_full=False
			output.append(dst_w[i]+'_'+dst_tags[i])
		writer.write(' '.join(output)+'\n')
	except:
		print alignment
		print dst_tags

writer.flush()
writer.close()
sys.stdout.write('\n')
