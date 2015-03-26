from __future__ import unicode_literals
import os,sys,codecs
from hazm import Normalizer,sent_tokenize, word_tokenize


reader=codecs.open(os.path.abspath(sys.argv[1]),'r',encoding='utf-8')
writer=codecs.open(os.path.abspath(sys.argv[2]),'w',encoding='utf-8')

count=1
line=reader.readline()

normalizer = Normalizer()

while line:
	if count%1000==0:
		sys.stdout.write(str(count)+'...')

	if line.strip():
		n=normalizer.normalize(line.strip())
		tok=word_tokenize(n)
		sen=u' '.join(tok)
		l=sen+u'\n'
		writer.write(l)
	else:
		writer.write(u'\n')

	count+=1
	line=reader.readline()
sys.stdout.write('\n')
writer.flush()
writer.close()