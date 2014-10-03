import os,sys,math
from collections import defaultdict

if len(sys.argv)<4:
	print 'python get_align_from_diag_file.py [src_file] [dst_file] [diag_file]'

reader1=open(os.path.abspath(sys.argv[1]),'r')
reader2=open(os.path.abspath(sys.argv[2]),'r')
diag_reader=open(os.path.abspath(sys.argv[3]),'r')

all_count=0

src_word_count=defaultdict(int)
dst_word_count=defaultdict(int)
joint_word_count=defaultdict(int)
writer=open(os.path.abspath(sys.argv[4]),'w')

line=diag_reader.readline()

line_num=0
while line:
	alg=line.strip().split(' ')
	line1=reader1.readline().strip()
	words1=line1.split(' ')
	line2=reader2.readline().strip()
	words2=line2.split(' ')

	alignement=[0]*len(words1)

	for i in range(0,len(alg)):
		fields=alg[i].split('-')
		src=int(fields[0])-1
		dst=int(fields[1])-1
		try:
			if src>=0 and dst>=0:
				alignement[src]=dst
		except:
			print src,dst
			print words1
			sys.exit(0)

	for word in words1:
		src_word_count[word]+=1
	for word in words2:
		dst_word_count[word]+=1
	all_count+=len(words1)+len(words2)

	for i in range(0,len(words1)):
		joint_word_count[words1[i]+'\t'+words2[alignement[i]]]+=1

	line_num+=1
	if line_num%10000==0:
		sys.stdout.write(str(line_num)+'...')
		sys.stdout.flush()
	line=diag_reader.readline()

sys.stdout.write('\n')
cnt=0
for word_pair in joint_word_count.keys():
	flds=word_pair.split('\t')
	src=flds[0]
	dst=flds[1]

	p_xy=float(joint_word_count[word_pair])/all_count
	p_x=float(src_word_count[src])/all_count
	p_y=float(dst_word_count[dst])/all_count

	pmi=math.log(p_xy)-math.log(p_x)-math.log(p_y)
	pmi2=2*math.log(p_xy)-math.log(p_x)-math.log(p_y)

	if src_word_count[src]>5 and dst_word_count[dst]>5:
		writer.write(word_pair+'\t'+str(src_word_count[src])+'\t'+str(dst_word_count[dst])+'\t'+str(pmi)+'\t'+str(pmi2)+'\n')
	cnt+=1
	if cnt%10000==0:
		sys.stdout.write(str(cnt)+'...')
		sys.stdout.flush()
sys.stdout.write('\n')

writer.flush()
writer.close()




