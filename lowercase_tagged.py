import os,sys,codecs,math

r1 = codecs.open(os.path.abspath(sys.argv[1]),'r')
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')
l1 = r1.readline()

while l1:
	output = list()
	for w_t in l1.strip().split():
		i = w_t.rfind('_')
		w = w_t[:i].lower()
		t = w_t[i+1:]
		output.append(w+'_'+t)
	writer.write(' '.join(output)+'\n')
	l1 = r1.readline()
writer.close()