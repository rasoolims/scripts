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
	belong = [defaultdict(str) for i  in xrange(len(dst_words))]
	can_belong = [defaultdict(str) for i  in xrange(len(dst_words))]
	for i in xrange(len(dst_words)):
		last_seen = -1
		for j in range(i+1,len(dst_words)):
			if dst_num[i]==dst_num[j] and dst_num[j]!=0:
				belong[i][j]=dst_phrase[j]
				belong[j][i]=dst_phrase[i]
				last_seen = dst_num[j]
			elif dst_num[j]==0 and dst_num[i]!=0:
				belong[i][j]=dst_phrase[j]
				belong[j][i]=dst_phrase[i]
				last_seen = dst_num[i]
			elif dst_num[i]==0:
				if dst_num[j] == 0:
					can_belong[i][j]=dst_phrase[j]
					can_belong[j][i]=dst_phrase[i]
				elif dst_num[j]!=0 and (last_seen==-1 or last_seen==dst_num[j]):
					last_seen = dst_num[j]
					can_belong[i][j]=dst_phrase[j]
					can_belong[j][i]=dst_phrase[i]
				else: break
			else: break

	for i in xrange(len(dst_words)):
		os = dst_words[i]+' '+dst_tags[i]
		bs = '_' if len(belong[i])==0 else ''
		for k in belong[i].keys():
			bs+= str(k)+'_'+belong[i][k]+','
		cbs = '_' if len(can_belong[i])==0 else ''
		for k in can_belong[i].keys():
			cbs+= str(k)+'_'+can_belong[i][k]+','
		output.append(os+' '+bs+' '+cbs)
	writer.write('\n'.join(output)+'\n\n') 

writer.close()
sys.stdout.write('\n')
