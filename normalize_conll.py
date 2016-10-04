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
	spl=line.strip().split('\t')
	if len(spl) > 2:
		spl[1] = get_clean_word(spl[1]);

	writer.write('\t'.join(spl)+'\n')

	line=reader.readline()
writer.flush()
writer.close()
