import os,sys,codecs,pickle,math
from collections import defaultdict
import numpy as np

def get_segments(bios):
	segments = []
	s, e, l = 0, 0, ''
	r = False
	for i in xrange(len(bios)):
		if bios[i] == 'O':
			if r:
				segments.append((s, e, bios[i - 1][bios[i - 1].find('-') + 1:]))
			segments.append((i, i, bios[i]))
			r = False
			s,e = i + 1,i + 1
		elif bios[i].startswith('B-') and r:
			segments.append((s, e, bios[i - 1][bios[i - 1].find('-') + 1:]))
			r = False
			s,e = i,i
		else:
			e = i
			r = True
	if r: 
		segments.append((s, e, bios[-1][bios[-1].find('-') + 1:]))
	return segments

def read_corpus_segments(f):
	sx = codecs.open(f,'r').read().strip().split('\n\n')
	bios_list = []
	for s in sx:
		lx = s.strip().split('\n')
		words,tags,bios = [],[],[]
		for i in xrange(len(lx)):
			spl = lx[i].strip().split()
			words.append(spl[0])
			tags.append(spl[1])
			bios.append(spl[2])
		bios_list.append(bios)
	return bios_list

def read_raw_corpus(f):
	sx = codecs.open(f,'r').read().strip().split('\n')
	sentences = []
	for s in sx:
		words = s.strip().split()
		for j in xrange(len(words)):
			words[j] = str(j+1)+':'+words[j]
		sentences.append(s.strip()+'\n'+ ' '.join(words))
	return sentences

def read_alignments(f):
	r = open(f,'r')
	line = r.readline()
	a_s = []
	while line:
		a = dict()
		for s in line.strip().split():
			src,trg = s.split('-')
			if int(src)!=0: a[int(src)-1] = int(trg) -1

		a_s.append(a)
		line = r.readline()
	return a_s

def bios2bios_align(bios, a):
	a_bios = []
	for i in xrange(len(bios)):
		if i in a:
			a_bios.append(bios[i]+'_'+str(a[i]+1))
		else:
			a_bios.append(bios[i]+'_*')
	return a_bios

if __name__ == "__main__":

	if len(sys.argv)<4:
		print 'directory target_lang output_file'
		sys.exit(0)
	dr = os.path.abspath(sys.argv[1])+'/'
	target_lang = sys.argv[2]
	writer = codecs.open(os.path.abspath(sys.argv[3]),'w')
	src_langs = ['ar',  'bg',  'cs',  'da',  'de',  'en',  'es',  'et',  'eu',  'fa',  'fi',  'fr',  'he',  'hi',  'hr',  'id',  'it',  'ja',  'ko',  'la',  'lv',  'nl',  'no',  'pl',  'pt',  'ro',  'ru',  'sk',  'sl',  'sv',  'tr',  'zh']
	
	sen_align_dict = defaultdict(list)


	for s in src_langs:
		if s == target_lang: continue
		print s
		dir_path = dr + s + '_'+target_lang+'/'
		if os.path.exists(dr + target_lang + '_'+s): dir_path = dr + target_lang + '_'+s+'/'

		a_s = read_alignments(dir_path + s + '_' + target_lang+'.intersect')
		target_sentences = read_raw_corpus(dir_path+'corpus.tok.clean.'+target_lang)
		src_bios = read_corpus_segments(dir_path+'corpus.tok.clean.'+s+'.chunk')
		dst_bios = read_corpus_segments(dir_path+'corpus.tok.clean.'+target_lang+'.chunk')
		for index in xrange(len(a_s)):
			indexed_bios = [str(i+1)+':'+dst_bios[index][i] for i in xrange(len(dst_bios[index]))]
			sen_align_dict[target_sentences[index]+'\nsupervised:\n'+' '.join(indexed_bios)].append('source:'+s+'\n'+' '.join(bios2bios_align(src_bios[index], a_s[index])))


	for sen in sen_align_dict.keys():
		writer.write(sen+'\n\n')
		for bios in sen_align_dict[sen]:
			writer.write(bios+'\n')
		writer.write('**************************************************\n')
	writer.close()
	print 'done!'
