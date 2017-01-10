import os,sys,math,operator,codecs,traceback
from collections import defaultdict

def sen2chunk(sen):
	lines = sen.strip().split('\n')
	words,tags,ctags = [],[],[]
	for line in lines:
		spl = line.strip().split()
		words.append(spl[0])
		tags.append(spl[1])
		ctags.append(spl[2])
	indicators = []

	for i in xrange(len(words)):
		prev = ctags[i-1] if i>0 else '<s>'
		next = ctags[i+1] if i<len(words)-1 else '</s>'
		indicators.append(prev + ctags[i] + next) 

	sen_words = ' '.join(words)
	return sen_words, words, tags, ctags, indicators

def chunk2output(words, tags, ctags):
	output = []
	for i in xrange(len(words)):
		output.append(words[i]+' '+tags[i]+' '+ctags[i])
	return '\n'.join(output)+'\n\n'

chunk_dict = dict()

print 'reading'
input_folder = os.path.abspath(sys.argv[1])+'/'
for f in os.listdir(input_folder):
	lang = f[f.rfind('2')+1:]
	print f
	if not lang in chunk_dict:
		chunk_dict[lang] = defaultdict(list)
	for sen in codecs.open(input_folder+f,'r').read().strip().split('\n\n'):
		if not sen.strip(): continue
		sen_words, words, tags, ctags, indicators = sen2chunk(sen)
		chunk_dict[lang][sen_words].append([words, tags, ctags, indicators])

output_path = os.path.abspath(sys.argv[2])+'/'
for lang in chunk_dict.keys():
	print 'voting',lang
	writer = codecs.open(output_path+lang,'w')
	for sen_words in chunk_dict[lang].keys():
		raw_votes = [defaultdict(int) for i in xrange(len(sen_words.split()))]
		votes = chunk_dict[lang][sen_words]
		words,tags = [],[]
		for vote in votes:
			[words, tags, ctags, indicators] = vote
			for i in xrange(len(ctags)):
				raw_votes[i][ctags[i]] += 1
		
		max_votes = []
		for i in xrange(len(raw_votes)):
			max_vote = 0
			max_chunk = '_'
			for ctag in raw_votes[i].keys():
				if ctag != '_' and max_vote<raw_votes[i][ctag]:
					max_vote = raw_votes[i][ctag]
					max_chunk = ctag
			max_votes.append(max_chunk)

		writer.write(chunk2output(words,tags,max_votes))
	writer.close()



