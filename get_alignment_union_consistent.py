import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<4:
	print 'python get_alignment_union_consistent.py [dst_sentences] [src_alignment] [dst_alignment] [output_file]'
	sys.exit(0)

reader0=codecs.open(os.path.abspath(sys.argv[1]),'r')
reader1=codecs.open(os.path.abspath(sys.argv[2]),'r')
reader2=codecs.open(os.path.abspath(sys.argv[3]),'r')
writer=open(os.path.abspath(sys.argv[4]),'w')


dst_sen_len = list()
line = reader0.readline()
while line:
	dst_sen_len.append(len(line.strip().split(' ')))
	line = reader0.readline()

src_alignments=defaultdict(set)
line1=reader1.readline()
line_num=0
while line1:
	line1=line1.strip()
	if line1.startswith('NULL ('):
		line_num+=1
		if line_num%10000==0:
			sys.stdout.write(str(line_num)+'...')
			sys.stdout.flush()
		flds=line1.replace('}) ','})\t').split('\t')
		
		src_to_dst_alignment = ['*']* (dst_sen_len[line_num-1]+1)
		src_to_dst_alignment[0]=0
		#ignoring null
		
		for i in range(1,len(flds)): 
			spls=flds[i].split(' ')
			j = 0
			for spl in spls:
				j +=1
				if spl.isdigit() and j>1:
					a=int(spl)
					#print i, a, dst_sen_len[line_num-1]
					src_to_dst_alignment[i]=a
		src_alignments[line_num]=src_to_dst_alignment
		#print '******'
	line1=reader1.readline()

sys.stdout.write('\n')

dst_alignments=defaultdict(set)
line2=reader2.readline()
line_num=0
while line2:
	line2=line2.strip()
	if line2.startswith('NULL ('):
		line_num+=1
		if line_num%10000==0:
			sys.stdout.write(str(line_num)+'...')
			sys.stdout.flush()
		flds=line2.replace('}) ','})\t').split('\t')

		dst_to_src_alignment = ['*']* (dst_sen_len[line_num-1]+1)
		dst_to_src_alignment[0]=0
		#ignoring null
		for i in range(1,len(flds)): 
			spls=flds[i].split(' ')
			j = 0 
			for spl in spls:
				j +=1
				if spl.isdigit() and j>1:
					a=int(spl)
					#print j,i, a, dst_sen_len[line_num-1]
					dst_to_src_alignment[a]=i
		#print '******'
		dst_alignments[line_num]=dst_to_src_alignment
	line2=reader2.readline()
sys.stdout.write('\n')

for i in src_alignments.keys():
	set1=src_alignments[i]
	set2=dst_alignments[i]

	union_set = list()
	for j in range(0,len(set1)):
		if set1[j]==set2[j] and set1[j]!='*':
			outp = str(set1[j])+'-'+str(j)
			union_set.append(outp)
		elif set1[j]=='*' and set2[j]!='*':
			outp = str(set2[j])+'-'+str(j)
			union_set.append(outp)
		elif set1[j]!='*' and set2[j]=='*':
			outp = str(set1[j])+'-'+str(j)
			union_set.append(outp)

	writer.write(' '.join(union_set)+'\n')
	if i%10000==0:
		sys.stdout.write(str(i)+'...')
		sys.stdout.flush()
writer.flush()
writer.close()
sys.stdout.write('\ndone\n')