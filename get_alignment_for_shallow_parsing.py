import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<4:
	print 'python get_alignment_for_shallow_parsing.py [src_alignment] [dst_alignment] [output_file]'
	sys.exit(0)


reader1=codecs.open(os.path.abspath(sys.argv[1]),'r')
reader2=codecs.open(os.path.abspath(sys.argv[2]),'r')
writer1=open(os.path.abspath(sys.argv[3])+'.e2f','w')
writer2=open(os.path.abspath(sys.argv[3])+'.f2e','w')

src_alignments = defaultdict(list)
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
					src_alignments[line_num].append(str(i)+'-'+str(a))
	line1=reader1.readline()

sys.stdout.write('\n')

dst_alignments=defaultdict(list)
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
					dst_alignments[line_num].append(str(a)+'-'+str(i))
	line2=reader2.readline()
sys.stdout.write('\n')

for i in src_alignments.keys():
	writer1.write(' '.join(src_alignments[i])+'\n')
	writer2.write(' '.join(dst_alignments[i])+'\n')

writer1.close()
writer2.close()
sys.stdout.write('\ndone\n')