import os,codecs,sys

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')

counter=1
labels=dict()


line=reader.readline()
count=0
while line:
	line=line.strip()
	if line:
		count+=1
		if count%10000==0:
			sys.stdout.write(str(count)+'('+str(counter)+')...')
		spl=line.split('\t')
		output=list()
		label='-1' if spl[-1]=='0' else '1'
		output.append(label)
		for f in range(0,len(spl)-1):
			feat=spl[f]
			label=str(counter)
			if labels.has_key(feat):
				label=str(labels[feat])
			else:
				labels[feat]=counter
				counter+=1
			output.append(label+':1')

		writer.write(' '.join(output)+'\n')


	line=reader.readline()
sys.stdout.write('\n')
writer.flush()
writer.close()