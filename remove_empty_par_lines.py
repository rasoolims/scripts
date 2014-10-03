import os,sys,codecs

reader1=open(os.path.abspath(sys.argv[1]),'r')
reader2=open(os.path.abspath(sys.argv[2]),'r')

writer1=open(os.path.abspath(sys.argv[3]),'w')
writer2=open(os.path.abspath(sys.argv[4]),'w')

line1=reader1.readline()
while line1:
	line2=reader2.readline()

	if line1.strip() and line2.strip():
		writer1.write(line1.strip()+'\n')
		writer2.write(line2.strip()+'\n')

	line1=reader1.readline()

writer1.flush()
writer2.flush()
writer1.close()
writer2.close()