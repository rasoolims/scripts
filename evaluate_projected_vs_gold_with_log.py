import os,sys,codecs
from collections import defaultdict
from termcolor import colored

if len(sys.argv)<3:
	print 'python evaluate_projected_vs_gold_with_log.py [proj mst] [gold mst] [gold_src_mst] [intersection-file] [src_map_file] [dst_map_file]'
	print 'two files do not need to be in the same size/order'
	sys.exit(0)

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


def is_punc(pos):
	return pos=="#" or pos=="$" or pos=="''" or pos=="(" or pos=="" or pos=="[" or pos=="]" or pos=="{" or pos=="}" or pos=="\"" or pos=="," or pos=="." or pos==":" or pos=="``" or pos=="-LRB-" or pos=="-RRB-" or pos=="-LSB-" or pos=="-RSB-" or pos=="-LCB-" or pos=="-RCB-"

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


projected_trees=defaultdict(list)
line_count=0
reader=codecs.open(os.path.abspath(sys.argv[1]),'r')

line=reader.readline()
while line:
	line=line.strip()
	if line:
		line_count+=1
		words=line.split('\t')
		tags=reader.readline().strip().split('\t')
		labels=reader.readline()
		hds=reader.readline().strip().split('\t')
		sentence=' '.join(words)

		hs=list()
		for h in hds:
			hs.append(str(int(round(float(h)))))

		hds=hs

		projected_trees[sentence].append([hds,tags,words])


	line=reader.readline()

gold_trees=defaultdict()
line_count=0
reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
reader2=codecs.open(os.path.abspath(sys.argv[3]),'r')
reader3=codecs.open(os.path.abspath(sys.argv[4]),'r')

src_pos_map=read_pos_map(os.path.abspath(sys.argv[5]))
dst_pos_map=read_pos_map(os.path.abspath(sys.argv[6]))

line=reader.readline()
line2=reader2.readline()
while line:
	line=line.strip()
	line2=line2.strip()
	if line:
		line3=reader3.readline().strip()
		line_count+=1
		words=line.split('\t')
		words2=line2.split('\t')
		alignment=[-1]*len(words)
		#print words
		#print words2
		#print line3
		#print len(words)
		#print len(words2)
		#print len(alignment)
		try:
			spl=line3.split(' ')
			for x in spl:
				#print x
				spl2=x.split('-')
				s1=int(spl2[0])
				s2=int(spl2[1])
				if s2!=0:
					alignment[s2-1]=s1-1
		except:
			alignment=[-1]*len(words)
		tags=reader.readline()
		tags2=reader2.readline().strip().split('\t')
		labels=reader.readline()
		labels2=reader2.readline()
		hds=reader.readline().strip().split('\t')
		hds2=reader2.readline().strip().split('\t')
		sentence=' '.join(words)

		hs=list()
		for h in hds:
			hs.append(int(h))
		hds=hs
		
		if not gold_trees.has_key(sentence):
			gold_trees[sentence]=[hds,words2,tags2,hds2,labels2,alignment]


	line=reader.readline()
	line2=reader2.readline()


correct=0
all_dep=0
line_count=0

all_partial=0
partial_correct=0

local_percent=0.0
all_num=0
max_local_percent=0.0
min_local_percent=1.0
min_change=10000
max_change=0
avg_change=0.0
change_diag=defaultdict(int)

for sentence_list in projected_trees.keys():
	for sentence in projected_trees[sentence_list]:
		if gold_trees.has_key(sentence_list):

			output=list()

			gh=gold_trees[sentence_list][0]
			gw=gold_trees[sentence_list][1]
			gp=gold_trees[sentence_list][2]
			gsh=gold_trees[sentence_list][3]
			alignment=gold_trees[sentence_list][5]
			ph=sentence[0]
			tags=sentence[1]
			words=sentence[2]

			print ' '.join(gw)
			print ' '.join(gp)
			print ' '.join(gsh)
			for i in range(0,len(words)):
				out=''
				s_h='_'
				s_m='_'
				sm_t='_'
				sh_t='_'
				head_pos_violated=''
				dep_pos_violated=''

				t_h='_'
				t_m=tags[i]
				if dst_pos_map.has_key(t_m):
					t_m=dst_pos_map[t_m]


				if gh[i]!=-1:
					if gh[i]==0:
						t_h='root'
					else:
						t_h=tags[gh[i]-1]

				if alignment[i]!=-1:
					sm_t=gp[alignment[i]]
					s_m=gw[alignment[i]]
					xh=int(gsh[alignment[i]])
					if xh==0:
						s_h='root'
					else:
						s_h=gw[xh-1]
						sh_t=gp[xh-1]

				if dst_pos_map.has_key(t_h):
					t_h=dst_pos_map[t_h]
				if src_pos_map.has_key(sm_t):
					sm_t=src_pos_map[sm_t]
				if src_pos_map.has_key(sh_t):
					sh_t=src_pos_map[sh_t]

				if not same_pos_kind(t_h,sh_t) and sh_t!='_' and t_h!='_' and sm!=words[i]:
					head_pos_violated='head_pos_mismatch'
				if not same_pos_kind(t_m,sm_t) and sm_t!='_' and t_m!='_':
					dep_pos_violated='dep_pos_mismatch'
				viol=(dep_pos_violated+'\t'+head_pos_violated).strip()

				if ph[i]=='-1':
					out='^'+str(i+1)+'\t'+words[i]+'\t'+tags[i]+'\t'+ph[i]+'\t'+str(gh[i])+'\t'+s_m+'('+s_h+')\t'+viol
				elif ph[i]==str(gh[i]):
					if viol=='':
						out=str(i+1)+'\t'+words[i]+'\t'+tags[i]+'\t'+ph[i]+'\t'+str(gh[i])+'\t'+s_m+'('+s_h+')\t'+viol
					else:
						out=colored(str(i+1)+'\t'+words[i]+'\t'+tags[i]+'\t'+ph[i]+'\t'+str(gh[i])+'\t'+s_m+'('+s_h+')\t'+viol,'green')
				else:
					out=colored('***'+str(i+1)+'\t'+words[i]+'\t'+tags[i]+'\t'+ph[i]+'\t'+str(gh[i])+'\t'+s_m+'('+s_h+')\t'+viol,'red')
				output.append(out)
			print '\n'.join(output)+'\n'
