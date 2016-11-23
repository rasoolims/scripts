import os,sys,codecs

def read_sentences(path):
	sentences = codecs.open(path,'r').read().strip().split('\n\n')

	for sentence in sentences:
		lines = sentence.strip().split('\n')
		sen_words = []
		for line in lines:
			sen_words.append((line.split()))
		yield sen_words

def bio2se(path):
	begin = 'B'
	inside = 'I'
	for sentence in read_sentences(path):
		new_sen = []
		for i in xrange(len(sentence)):
			s = sentence[i][2][0]
			nxt = sentence[i+1][2][0] if i<len(sentence)-1 else begin
			
			new_tag = 'B'+sentence[i][2][1:]
			if s==begin and nxt==begin:
				new_tag = 'S'+sentence[i][2][1:]
			elif s==inside and nxt==begin:
				new_tag = 'E'+ sentence[i][2][1:]
			elif s==inside and nxt==inside:
				new_tag = 'I'+ sentence[i][2][1:]
			new_sen.append((sentence[i][0],sentence[i][1],new_tag))
		yield new_sen

def sen2output(sentence):
	output = []
	for sen in sentence:
		output.append(' '.join(sen))
	return '\n'.join(output)+'\n\n'

def __main__(inp_path, output_path):
	writer = codecs.open(output_path, 'w')
	for sentence in bio2se(inp_path):
		writer.write(sen2output(sentence))
	writer.close()


if __name__ == "__main__":
	__main__(os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2]))

