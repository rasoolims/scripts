import os,sys,codecs

def get_clean_word(word):
	if word=='-LRB-':
		return '('
	if word=='-RRB-':
		return ')'
	if word=='-LCB-':
		return '{'
	if word=='-RCB-':
		return '}'
	if word=='-LSB-':
		return '['
	if word == '-RSB-':
		return ']'
	return word


reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')

count=0
line=reader.readline()
while line:
	spl=line.strip().split(' ')
	output=list()
	for s in spl:
		output.append(get_clean_word(s.strip()))
	writer.write(' '.join(output)+'\n')
	count+=1
	if count%1000000==0:
		sys.stdout.write(str(count/1000000)+'M...')
	line=reader.readline()
writer.flush()
writer.close()
sys.stdout.write(str(count)+'\n')
