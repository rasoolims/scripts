import os,sys

reader1=open(os.path.abspath(sys.argv[1]),'r')
reader2=open(os.path.abspath(sys.argv[2]),'r')
writer1=open(os.path.abspath(sys.argv[3]),'w')
writer2=open(os.path.abspath(sys.argv[4]),'w')

line1=reader1.readline()
while line1:
  line2=reader2.readline()

  len1=len(line1.strip().split(' '))
  len2=len(line2.strip().split(' '))

  if len1<100 and len2<100 and len1/len2<9 and len2/len1<9:
    writer1.write(line1.strip()+'\n')
    writer2.write(line2.strip()+'\n')

  line1=reader1.readline()

writer1.flush()
writer2.flush()
writer1.close()
writer2.close()