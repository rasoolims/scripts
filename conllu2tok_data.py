# coding: utf8
import os,sys,codecs,re

h_sens = codecs.open(os.path.abspath(sys.argv[1]),'r',encoding='utf-8').read().strip().split('\n\n')
writer = codecs.open(os.path.abspath(sys.argv[2]),'w',encoding='utf-8')

ignored = 0
for h_sen in h_sens:
	lines = h_sen.strip().split('\n')
	raw = ''
	words = []

	for l in lines:
		if l.strip().startswith('# text ='):
			raw = l.strip()[8:].strip()
			raw = re.sub(r'\s+', ' ', raw)
		if not l.startswith('#'):
			if not '.' in l.strip().split()[0] and l.strip().split()[0].isdigit():
				words.append(l.strip().split()[1])

	tokenized = ' '.join(words).strip()


	raw = list(raw)
	tokenized = list(tokenized)
	
	r = 0
	t = 0

	output = []
	bad_code = False
	while r<len(raw) or t<len(tokenized):
		if raw[r]==tokenized[t]:
			output.append(raw[r])
			r+=1
			t+=1
		else:
			if tokenized[t]!=' ' and tokenized!=u'‌':
				bad_code = True
				break
			output.append('<SPLIT>')
			t+=1

	if not bad_code: 
		writer.write(u''.join(output)+'\n')
	if bad_code:
		ignored+=1
		print ''.join(raw)
		print ''.join(tokenized)
		print ''.join(output)
print 'ignored',ignored,'out of',len(h_sens)