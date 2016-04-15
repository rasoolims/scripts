import os,sys,codecs

reader1=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer1=codecs.open(os.path.abspath(sys.argv[2]),'w')


line1=reader1.readline()
all_count = 0
count = 0

while line1:
	spl=line1.strip().split('\t')
	if len(spl)>2:
		if spl[9]!='_' and spl[1]!=spl[2]:
			spl[1]='_'
			count+=1
		if spl[9]!='_':
			all_count+=1
		writer1.write('\t'.join(spl)+'\n')
	else:
		writer1.write(line1)
	line1=reader1.readline()
writer1.close()
print count,all_count