import os,sys,math,operator,codecs,traceback
from collections import defaultdict

if len(sys.argv)<5:
	print 'python project_shallow_trees.py [src_shallow_file] [dst_tag_file] [align_file] [output_file_name]'
	sys.exit(0)

print 'reading src trees'
src_trees = codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')
print 'reading dst sentences'
dst_sentences = codecs.open(os.path.abspath(sys.argv[2]),'r').read().strip().split('\n')

align_reader=codecs.open(os.path.abspath(sys.argv[3]),'r')
output_file_name=os.path.abspath(sys.argv[4])

use_fill_heuristic = True
if len(sys.argv)>5 and sys.argv[5]=='false':
	use_fill_heuristic = False

src_alignment_dic=defaultdict()

# reading line by line alignments
line_count=0
sys.stdout.write('reading alignments...')
sys.stdout.flush()
line=align_reader.readline()
while line:
	line=line.strip()
	if line:
		src_alignment_dic[line_count]=defaultdict()

		flds=line.split(' ')
		for fld in flds:
			split_flds=fld.split('-')
			src_index=int(split_flds[0])
			dst_index=int(split_flds[1])
			src_alignment_dic[line_count][src_index]=dst_index
		if line_count%100000==0:
			sys.stdout.write(str(line_count)+'...')
		line_count+=1
	line=align_reader.readline()
sys.stdout.write('\n')


# initializing different types of outputs
writer = codecs.open(output_file_name,'w')
writer2 = codecs.open(output_file_name+'.log','w')

print 'getting src projections...'
num_full = 0

for sa in src_alignment_dic.keys():
	if sa%10000==0:
		sys.stdout.write(str(sa)+'...')
	alignment = src_alignment_dic[sa]

	dst_words = []
	dst_tags = []
	for tok in dst_sentences[sa].strip().split(' '):
		ind = tok.rfind('_')
		dst_words.append(tok[:ind])
		dst_tags.append(tok[ind+1:])

	src_words = []
	src_tags = []
	src_phrase = []
	src_num = []
	ind = 0

	for tok in src_trees[sa].strip().split('\n'):
		w,t,ph = tok.strip().split()
		src_words.append(w)
		src_tags.append(t)
		src_phrase.append(ph)
		if ph.startswith('B-'):
			ind+=1
		src_num.append(str(ind))

	cand_alignment = dict()
	cand_num = dict()
	for s in alignment.keys():
		cand_alignment[alignment[s]-1] = src_phrase[s-1]
		cand_num[alignment[s]-1] = src_num[s-1]

	dst_phrase = []
	dst_num = []
	seen_phrases = defaultdict(list)
	for i in xrange(len(dst_words)):
		if cand_alignment.has_key(i):
			dst_phrase.append(cand_alignment[i])
			dst_num.append(cand_num[i])
			seen_phrases[cand_num[i]].append(i)
		else:
			dst_phrase.append('_')
			dst_num.append(0)

	output = []
	[output.append(dst_words[i]+' '+dst_tags[i]+' '+dst_phrase[i]+'-'+str(dst_num[i])) for i in xrange(len(dst_words))]
	writer2.write('\n'.join(output)+'\n\n') 

	consistents = dict()
	for seen_phrase in seen_phrases.keys():
		seen_sorted = sorted(seen_phrases[seen_phrase])
		consistent = True
		for i in range(seen_sorted[0],seen_sorted[-1]):
			if dst_num[i] != seen_phrase:
				consistent = False
				break
		consistents[seen_phrase] = consistent

	for seen_phrase in seen_phrases.keys():
		consistent = consistents[seen_phrase]
		if consistent:
			writer2.write(str(seen_phrase)+'\n')
			seen_sorted = sorted(seen_phrases[seen_phrase])
			for ss in seen_sorted:
				writer2.write(str(ss)+',')
			writer2.write('\n')
			for i in range(seen_sorted[0],seen_sorted[-1]):
				if dst_num[i]==0:
					dst_num[i] = seen_phrase
					dst_phrase[i] = dst_phrase[seen_sorted[0]]
			writer2.write('->'+str(seen_sorted[0])+'->B\n')
			dst_phrase[seen_sorted[0]]='B-'+dst_phrase[seen_sorted[0]][2:]
			for i in range(seen_sorted[0]+1,seen_sorted[-1]+1):
				dst_phrase[i]='I-'+dst_phrase[i][2:]
				writer2.write('->'+str(i)+'->I\n')

			if len(seen_phrases[seen_phrase])==1:
				dst_phrase[seen_sorted[0]]='B-'+dst_tags[seen_sorted[0]]+'P'
		else:
			for i in seen_phrases[seen_phrase]:
				dst_num[i]=0
				dst_phrase[i]='_'

	# completing empty singletons (heuristic!)
	if use_fill_heuristic:
		to_add = []
		for i in xrange(len(dst_words)):
			if dst_num[i]== 0:
				if (i==0 or dst_num[i-1]!=0) and (i==len(dst_words)-1 or dst_num[i+1]!=0):
					to_add.append(i)
		for i in to_add:
			dst_phrase[i]='B-'+dst_tags[i]+'P'

	is_full = True
	for i in xrange(len(dst_words)):
		if dst_num[i]== 0:
			is_full = False
			break
	if is_full:
		num_full +=1

	output = []
	[output.append(dst_words[i]+' '+dst_tags[i]+' '+dst_phrase[i]) for i in xrange(len(dst_words))]
	writer.write('\n'.join(output)+'\n\n') 
	

writer.close()
writer2.close()
sys.stdout.write('\n')
print num_full,len(src_alignment_dic)
