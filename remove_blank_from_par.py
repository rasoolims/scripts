import os,sys,codecs

reader1=codecs.open(os.path.abspath(sys.argv[1]),'r')
reader2=codecs.open(os.path.abspath(sys.argv[2]),'r')

writer1=codecs.open(os.path.abspath(sys.argv[3]),'w')
writer2=codecs.open(os.path.abspath(sys.argv[4]),'w')

line1=reader1.readline()
line2=reader2.readline()

while line1:

	if line1.strip() and line2.strip():
		writer1.write(line1)
		writer2.write(line2)
	line2=reader2.readline()
	line1=reader1.readline()

writer1.close()
writer2.close()
