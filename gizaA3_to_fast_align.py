import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<3:
	print 'python gizaA3_to_fast_align.py [alignment_file(A3.final)] [output_file] [flip]'
	sys.exit(0)

reader1=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer=open(os.path.abspath(sys.argv[2]),'w')
flip = False
if len(sys.argv)>3 and sys.argv[3]=='flip':
	flip = True

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
		al = list()
		for i in range(1,len(flds)): 
			spls=flds[i].split(' ')
			for spl in spls[1:]:
				if spl.isdigit():
					a=int(spl)

					als=str(i-1)+'-'+str(a-1)
					if flip:
						als=str(a-1)+'-'+str(i-1)
					al.append(als)
		writer.write(' '.join(al)+'\n')
	line1=reader1.readline()

sys.stdout.write('\n')

writer.flush()
writer.close()
sys.stdout.write('\ndone\n')