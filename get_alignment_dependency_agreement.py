import os,sys,math
from collections import defaultdict

if len(sys.argv)<4:
	print 'python get_alignment_dependency_agreement.py [src_mst_file] [dst_mst_file] [diag_file]'

reader1=open(os.path.abspath(sys.argv[1]),'r')
reader2=open(os.path.abspath(sys.argv[2]),'r')
diag_reader=open(os.path.abspath(sys.argv[3]),'r')
pmi_reader=open(os.path.abspath(sys.argv[4]),'r')


pmi_dic=defaultdict(float)
line=pmi_reader.readline()
counter=0
while line:
	flds=line.strip().split('\t')
	pair=flds[0]+'\t'+flds[1]

	pmi=float(flds[5])
	pmi_dic[pair]=pmi

	counter+=1
	if counter%100000==0:
		sys.stdout.write(str(counter)+'...')
		sys.stdout.flush()
	line=pmi_reader.readline()

uac=0
ac=0
all_c=0

all_count=0
print ''
src_word_count=defaultdict(int)
dst_word_count=defaultdict(int)
joint_word_count=defaultdict(int)
counter=0
line=diag_reader.readline()
while line:
	counter+=1
	if counter%10000==0:
		sys.stdout.write(str(counter)+'...')
		sys.stdout.flush()
	line1=reader1.readline().strip()
	while not line1:
		line1=reader1.readline().strip()
	words1=line1.split('\t')
	tags1=reader1.readline().strip().split('\t')
	labels1=reader1.readline().strip().split('\t')
	fileds=reader1.readline().strip().split('\t')
	heads1=list()
	for f in fileds:
		heads1.append(round(float(f)))

	line2=reader2.readline().strip()
	while not line2:
		line2=reader2.readline().strip()
	words2=line2.split('\t')
	tags2=reader2.readline().strip().split('\t')
	labels2=reader2.readline().strip().split('\t')
	fileds=reader2.readline().strip().split('\t')
	heads2=list()
	for f in fileds:
		heads2.append(round(float(f)))

	alignment=line.strip().split(' ')
	src_alignment_list=defaultdict(int)
	for alg in alignment:
		fls=alg.split('-')
		src=int(fls[0])
		dst=int(fls[1])

		if not src_alignment_list.has_key(src):
			src_alignment_list[src]=dst
		else:
			new_pair=''
			try:
				new_pair=words1[src]+'\t'+words2[dst]
			except:
				print words1
				print words2
				print src,dst
				print counter
				sys.exit(0)
			new_pmi=pmi_dic[new_pair]

			if new_pmi>pmi_dic[src_alignment_list[src]]:
				src_alignment_list[src]=dst

	for s in range(0,len(heads1)):
		d=s
		h=heads1[s]-1
		l=labels1[s]

		ah=-1
		if h>=0:
			ah=src_alignment_list[h]

		td=src_alignment_list[d]
		th=heads2[td]
		tl=labels2[td]

		if ah==th:
			uac+=1
			if tl==l:
				ac+=1
		all_c+=1



	line=diag_reader.readline()

print ''
print float(100*uac)/all_c
print float(100*ac)/all_c