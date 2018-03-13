import sys,os, codecs

reader1 = codecs.open(os.path.abspath(sys.argv[1]), 'r')
reader2 = codecs.open(os.path.abspath(sys.argv[2]), 'r')
writer = codecs.open(os.path.abspath(sys.argv[3]), 'w')

i = 0
line = reader1.readline()
while line:
	i+=1
	line2 = reader2.readline()
	writer.write(line.strip()+'\n')
	if i%4==0:
		writer.write(line2.strip()+'\n')

	line = reader1.readline()
writer.close()
