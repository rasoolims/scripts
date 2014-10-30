import os,sys

def standardize_column_separated(line):
	l=line.strip().replace(',','\t').split('\t')
	for i in range(0,len(l)-1):
		l[i]=str(i+1)+':'+l[i]
	f=list()
	for i in range(0,len(l)-1):
		f.append(l[i])
		for j in range(0,len(l)-1):
			f.append(l[i]+'|'+l[j])
	f.append(l[-1])
	return '\t'.join(f)


lines=open(os.path.abspath(sys.argv[1]),'r').read().split('\n')
writer=open(os.path.abspath(sys.argv[2]),'w')

for line in lines:
	writer.write(standardize_column_separated(line)+'\n')

writer.flush()
writer.close()

