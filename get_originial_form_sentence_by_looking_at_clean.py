import os,sys


if len(sys.argv)<6:
	print 'python get_originial_form_sentence_by_looking_at_clean.py [*.lid file] [source_file] [trg_file] [source_output_file] [trg_output_file]'
	sys.exit(0)

lids=open(os.path.abspath(sys.argv[1]),'r').read().split('\n')
useful_sens=set()
for lid in lids:
	if lid.strip():
		useful_sens.add(int(lid.strip()))

print len(useful_sens)

reader1=open(os.path.abspath(sys.argv[2]),'r')
reader2=open(os.path.abspath(sys.argv[3]),'r')
writer1=open(os.path.abspath(sys.argv[4]),'w')
writer2=open(os.path.abspath(sys.argv[5]),'w')


sen_num=1
line1=reader1.readline()
while line1:
	line2=reader2.readline()
	if sen_num in useful_sens:
		writer1.write(line1.replace(' | ',' ').replace('|','').strip()+'\n')
		writer2.write(line2.replace(' | ',' ').replace('|','').strip()+'\n')
	sen_num+=1
	if sen_num%100000==0:
		sys.stdout.write(str(sen_num)+'...')
	line1=reader1.readline()
sys.stdout.write('\ndone\n')

writer1.flush()
writer1.close()
writer2.flush()
writer2.close()