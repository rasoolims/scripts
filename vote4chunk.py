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
	sgs = []
	for s in sx:
		lx = s.strip().split('\n')
		words,tags,bios = [],[],[]
		for i in xrange(len(lx)):
			spl = lx[i].strip().split()
			words.append(spl[0])
			tags.append(spl[1])
			bios.append(spl[2])
		segments = get_segments(bios)
		sgs.append(segments)
	return sgs

def read_raw_corpus(f):
	sx = codecs.open(f,'r').read().strip().split('\n')
	sentences = []
	for s in sx:
		words = s.strip().split()
		sentences.append(words)
	return sentences

def get_matrix(segments):
	sl = segments[-1][1]+1
	matrix = [[0]*sl for _ in xrange(sl)]
	for seg in segments:
		s,e,l = seg
		for i in range(s,e+1):
			for j in range(s,e+1):
				matrix[i][j] = l
			for j in xrange(sl):
				if j<s or j>e:
					matrix[i][j] = 'S'
					matrix[j][i] = 'S'
	return matrix

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

def align_matrix(m, a, l):
	tm = [[0]*l for _ in xrange(l)]

	for i in xrange(len(m)):
		ai = a[i] if i in a else -1
		for j in xrange(len(m)):
			aj = a[j] if j in a else -1

			if ai!=-1 and aj!=-1:
				tm[ai][aj] = m[i][j]
	
	for i in xrange(l):
		for j in xrange(l):
			if tm[i][j]==0:
				tm[i][j] = "U"

	return tm

def viterbi_decoding_semi(tm):
	bp = []
	l = len(tm)
	tags = ['I','U','O']
	itags = {0:'I',1:'U',2:'O'}
	fwd = [[0]*len(tags)]* (l+1)

	for i in xrange(l):
		bpt = []
		vvars_t = []

		for next_tag in tags:
			max_pointer = 0
			max_value = float('-inf')
			
			for k in xrange(i+1):
				nt_expr = [0]*len(tags)
				best_tag_id = 0
				best_tag_value = float('-inf')
				for nt in xrange(len(tags)):
					nt_expr[nt] = fwd[k][nt] + tm[i][k][itags[nt]]
					if nt_expr[nt]> best_tag_value:
						best_tag_value = nt_expr[nt]
						best_tag_id = nt
					if best_tag_value>max_value:
						max_value = best_tag_value
						max_pointer = best_tag_id, k, best_tag_value
			bpt.append((max_pointer[0],max_pointer[1]))
			vvars_t.append(max_pointer[2])
		fwd[i+1] = vvars_t
		bp.append(bpt)
	best_tag_id = np.argmax(fwd[-1])
	segments = []
	end = l-1
	while end>=0:
		best_tag_id,start = bp[end][best_tag_id]
		segments.append((start,end,best_tag_id))
		end = start-1
	segments.reverse()

	bios = []
	for s,e,lab in segments:
		label = itags[lab]
		if label == 'O' or label == 'U':
			bios.append(label)
		else:
			bios.append('B-'+label)
		for se in range(s,e):
			if label == 'O' or label == 'U':
				bios.append(label)
			else:
				bios.append('I-' + label)

	return bios

def matrix2str(mat,label):
	output = []
	for i in xrange(len(mat)):
		o = []
		for j in xrange(len(mat[i])):
			o.append(str(mat[i][j][label]))
		output.append(' '.join(o))
	return '\n'.join(output)

if __name__ == "__main__":

	if len(sys.argv)<4:
		print 'directory target_lang output_file'
		sys.exit(0)
	dr = os.path.abspath(sys.argv[1])+'/'
	target_lang = sys.argv[2]
	outpath = os.path.abspath(sys.argv[3])
	src_langs = ['ar',  'bg',  'cs',  'da',  'de',  'en',  'es',  'et',  'eu',  'fa',  'fi',  'fr',  'he',  'hi',  'hr',  'id',  'it',  'ja',  'ko',  'la',  'lv',  'nl',  'no',  'pl',  'pt',  'ro',  'ru',  'sk',  'sl',  'sv',  'tr',  'zh']
	
	target_matrix_dict = dict()

	for s in src_langs:
		if s == target_lang: continue
		print s
		dir_path = dr + s + '_'+target_lang+'/'
		if os.path.exists(dr + target_lang + '_'+s): dir_path = dr + target_lang + '_'+s+'/'

		a_s = read_alignments(dir_path + s + '_' + target_lang+'.intersect')
		target_sentences = read_raw_corpus(dir_path+'corpus.tok.clean.'+target_lang)
		src_segments = read_corpus_segments(dir_path+'corpus.tok.clean.'+s+'.chunk')
		print len(target_sentences),len(src_segments),len(a_s)
		assert len(target_sentences) == len(src_segments) and len(src_segments)==len(a_s)

		for i_ in xrange(len(target_sentences)):
			sen = ' '.join(target_sentences[i_])
			l = len(target_sentences[i_])
			if not sen in target_matrix_dict:
				target_matrix_dict[sen] = [[defaultdict(int)]*l for _ in xrange(l)] 
			tm = align_matrix(get_matrix(src_segments[i_]), a_s[i_], l)

			for i in xrange(l):
				for j in xrange(l):
					target_matrix_dict[sen][i][j][tm[i][j]]+=1
					if tm[i][j] != 'O' and tm[i][j]!= 'U':
						target_matrix_dict[sen][i][j]['I']+=1


	writer = codecs.open(outpath, 'w')
	for sen in target_matrix_dict.keys():
		l = len(target_matrix_dict[sen])
		print sen
		new_tm = [[defaultdict(int)]*l for _ in xrange(l)] 
		for i in xrange(l):
			for j in xrange(l):
				for label in ['I','U','O']:
					if label == 'I':
						votes = 0
						for k in  range(i, j+1):
							votes+= target_matrix_dict[sen][k][j][label] - target_matrix_dict[sen][k][j]['O']
						new_tm[i][j][label] = votes + new_tm[i][j-1][label] if j>0 else 0
					else:
						new_tm[i][j][label] = target_matrix_dict[sen][i][j][label]
		
		for i in xrange(l):
			for j in xrange(l):
				if i<j: 
					new_tm[i][j]['O']= 0
		writer.write(matrix2str(target_matrix_dict[sen],'I')+'\n\n')
		writer.write(matrix2str(target_matrix_dict[sen],'O')+'\n\n')
		writer.write(matrix2str(target_matrix_dict[sen],'U')+'\n\n')
		writer.write(matrix2str(new_tm,'I')+'\n\n')
		writer.write(matrix2str(new_tm,'O')+'\n\n')
		bios =  viterbi_decoding_semi(new_tm)
		writer.write(sen+'\n')
		writer.write(' '.join(bios)+'\n\n')

	print 'done!'
