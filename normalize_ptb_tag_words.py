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

line=reader.readline()
while line:
	spl=line.strip().split(' ')
	output=list()
	for s in spl:
		wp=s.split('_')
		if len(wp)>1:
			output.append(get_clean_word(wp[0])+'_'+wp[1])
	writer.write(' '.join(output)+'\n')

	line=reader.readline()
writer.flush()
writer.close()
