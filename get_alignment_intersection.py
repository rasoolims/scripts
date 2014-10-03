import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<4:
	print 'python get_alignment_intersection.py [src_alignment] [dst_alignment] [output_file]'
	sys.exit(0)

reader1=codecs.open(os.path.abspath(sys.argv[1]),'r')
reader2=codecs.open(os.path.abspath(sys.argv[2]),'r')
writer=open(os.path.abspath(sys.argv[3]),'w')

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
		#ignoring null
		for i in range(1,len(flds)): 
			spls=flds[i].split(' ')
			for spl in spls:
				if spl.isdigit():
					a=int(spl)
					als=str(i)+'-'+str(a)
					src_alignments[line_num].add(als)
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

		#ignoring null
		for i in range(1,len(flds)): 
			spls=flds[i].split(' ')
			for spl in spls:
				if spl.isdigit():
					a=int(spl)
					als=str(a)+'-'+str(i)
					dst_alignments[line_num].add(als)
	line2=reader2.readline()
sys.stdout.write('\n')


for i in src_alignments.keys():
	set1=src_alignments[i]
	set2=dst_alignments[i]
	intersection=set1&set2
	intersection.add('0-0')
	writer.write(' '.join(intersection)+'\n')
	if i%10000==0:
		sys.stdout.write(str(i)+'...')
		sys.stdout.flush()
writer.flush()
writer.close()
sys.stdout.write('\ndone\n')