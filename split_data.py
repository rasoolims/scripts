import os,codecs,sys

input_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
train_writer=codecs.open(os.path.abspath(sys.argv[2]),'w')
dev_writer=codecs.open(os.path.abspath(sys.argv[3]),'w')


line=input_reader.readline()
cnt=0
while line:
	line=line.strip()
	if line:
		cnt+=1
		if cnt%10==0:
			dev_writer.write(line+'\n')
		else:
			train_writer.write(line+'\n')

		if cnt%100000==0:
			sys.stdout.write(str(cnt)+'...')
	line=input_reader.readline()

sys.stdout.write('\n')
dev_writer.flush()
dev_writer.close()
train_writer.flush()
train_writer.close()