import os,codecs,sys


if len(sys.argv)<3:
	print 'python prune_mst_by_length.py [src mst file] [dst mst file] [max_len]'
	sys.exit(0)

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')
max_len=int(sys.argv[3])

line_count=0
line=reader.readline()
while line:
	line=line.strip()
	if line:
		line_count+=1
		words=line.split('\t')
		tags=reader.readline().strip()
		labels=reader.readline().strip()
		hds=reader.readline().strip()

		if len(words)<=max_len:
			writer.write('\t'.join(words)+'\n')
			writer.write(tags+'\n')
			writer.write(labels+'\n')
			writer.write(hds+'\n\n')

		if line_count%10000==0:
			sys.stdout.write(str(line_count)+'...')



	line=reader.readline()

writer.flush()
writer.close()
sys.stdout.write('\n')
