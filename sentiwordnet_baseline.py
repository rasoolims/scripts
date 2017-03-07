import os,sys,codecs

print '[senti_word_net] [test_data]'
eval_script = os.path.dirname(os.path.abspath(sys.argv[0]))+'/eval_sentiment.py'

pos_dict = dict()
neg_dict = dict()
for line in  codecs.open(os.path.abspath(sys.argv[1]),'r'):
	if line.strip():
		word,pos,neg = line.strip().split('\t')
		pos_dict[word] = float(pos)
		neg_dict[word] = float(neg)

t = 0.1 if len(sys.argv)<4 else float(sys.argv[3])
writer = codecs.open('/tmp/output','w')
for line in codecs.open(os.path.abspath(sys.argv[2]),'r'):
	line = line.strip()
	if line:
		sen = line.split('\t')[0]
		f_pos, f_neg,c = 0.0,0.0,0
		for word in sen.split(' '):
			if word in pos_dict:
				f_pos += pos_dict[word]
				f_neg += neg_dict[word]
				c+=1
		if c>0:
			f_pos/=c
			f_neg/=c

		l = 'neutral'
		if f_pos-f_neg > t:
			l = 'positive'
		elif f_neg-f_pos > t:
			l = 'negative'

		writer.write(sen+'\t'+l+'\n')
writer.close()

print os.path.abspath(sys.argv[2])
command = 'python -u '+eval_script+' '+ os.path.abspath(sys.argv[2]) +' /tmp/output'
os.system(command)

