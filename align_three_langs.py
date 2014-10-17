import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<7:
	print 'python align_three_langs.py [src1_file] [dst1_file] [src2_file] [dst2_file] [src_output] [dst1_output] [dst2_output]'
	sys.exit(0)
src1_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
dst1_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')
src2_reader=codecs.open(os.path.abspath(sys.argv[3]),'r')
dst2_reader=codecs.open(os.path.abspath(sys.argv[4]),'r')

src_writer=codecs.open(os.path.abspath(sys.argv[5]),'w')
dst1_writer=codecs.open(os.path.abspath(sys.argv[6]),'w')
dst2_writer=codecs.open(os.path.abspath(sys.argv[7]),'w')


sen_dict=defaultdict(list)

#print 'reading from the first parallel data'
#sys.stdout.flush()
line1 =src1_reader.readline()
count=0
while line1:
	line1=line1.strip()
	line2=dst1_reader.readline().strip()

	sen_dict[line1]=list()
	sen_dict[line1].append(line2)

	count+=1
	#if count%100000==0:
		#sys.stdout.write(str(count)+'....')
		#sys.stdout.flush()
	line1 =src1_reader.readline()

#print '\nreading from the second parallel data'
#sys.stdout.flush()
line1 =src2_reader.readline()
count=0
while line1:
	line1=line1.strip()
	line2=dst2_reader.readline().strip()

	if sen_dict.has_key(line1) and len(sen_dict[line1])==1:
		sen_dict[line1].append(line2)

	count+=1
	#if count%100000==0:
		#sys.stdout.write(str(count)+'....')
		#sys.stdout.flush()

	line1 =src2_reader.readline()


#print '\nwriting the files'
#sys.stdout.flush()
count=0
for src_line in sen_dict.keys():
	if len(sen_dict[src_line])==2:
		src_writer.write(src_line+'\n')
		dst1_writer.write(sen_dict[src_line][0]+'\n')
		dst2_writer.write(sen_dict[src_line][1]+'\n')
		count+=1
		#if count%100000==0:
			#sys.stdout.write(str(count)+'....')
			#sys.stdout.flush()
print '\ndone with count:'+str(count)
sys.stdout.flush()