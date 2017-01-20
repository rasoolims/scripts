import os,sys,codecs

def sen2chunk(sen):
	lines = sen.strip().split('\n')
	ctags = []
	for line in lines:
		spl = line.strip().split()
		ctags.append(line.strip().split()[2])

	return ctags



sens = codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')
writer = [None]*11
dense_info = [0]*11
for i in xrange(len(writer)):
	writer[i] = codecs.open(os.path.abspath(sys.argv[2])+'.'+str(i),'w')
for sen in sens:
	ctags = sen2chunk(sen)
	density = float(len([tag for tag in ctags if tag!='_']))/len(ctags)
	if density==1.0:
		dense_info[0] = dense_info[0]+1
		writer[0].write(sen.strip()+'\n\n')
	elif density>=0.9:
		dense_info[1] = dense_info[1]+1
		writer[1].write(sen.strip()+'\n\n')
	elif density>=0.8:
		dense_info[2] = dense_info[2]+1
		writer[2].write(sen.strip()+'\n\n')
	elif density>=0.7:
		dense_info[3] = dense_info[3]+1
		writer[3].write(sen.strip()+'\n\n')
	elif density>=0.6:
		dense_info[4] = dense_info[4]+1
		writer[4].write(sen.strip()+'\n\n')
	elif density>=0.5:
		dense_info[5] = dense_info[5]+1
		writer[5].write(sen.strip()+'\n\n')
	elif density>=0.4:
		dense_info[6] = dense_info[6]+1
		writer[6].write(sen.strip()+'\n\n')
	elif density>=0.3:
		dense_info[7] = dense_info[7]+1
		writer[7].write(sen.strip()+'\n\n')
	elif density>=0.2:
		dense_info[8] = dense_info[8]+1
		writer[8].write(sen.strip()+'\n\n')
	elif density>=0.1:
		dense_info[9] = dense_info[9]+1
		writer[9].write(sen.strip()+'\n\n')
	else:
		dense_info[10] = dense_info[10]+1
		writer[10].write(sen.strip()+'\n\n')
for i in xrange(len(writer)):
	writer[i].close() 
print dense_info