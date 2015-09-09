#! /usr/bin/python

import codecs, os, sys

def get_spans_(words, tags, heads, deps, min_span):
	'''
		Having a partial tree, extracts sets of full spans. It also includes
		previous and next pos and pos and label for the span head.
	'''  
	if len(heads)==0:
		return ''

	assert len(heads) == len(deps)

	output_list = list()
	start_ranges = list()
	end_ranges = list()

	start_ranges.append(0)

	for i in range(0, len(heads)):
		if heads[i] == -1:
			end_ranges.append(i-1)
			if i !=len(heads)-1:
				start_ranges.append(i+1)
		elif i==len(heads)-1:
			end_ranges.append(i)

	# temp vars
	s_r = list()
	e_r = list()
	s_l = len(start_ranges)
	for i in range(0,s_l):
		span_size = end_ranges[i] - start_ranges[i] + 1 
		if span_size >= min_span:
			# can add all possible spans with at least two words here.
			for j in range(start_ranges[i],end_ranges[i]+1):
				for k in range(j+1,end_ranges[i]+1):
					s_r.append(j)
					e_r.append(k)

	start_ranges = s_r
	end_ranges = e_r

	for i in range(0,len(start_ranges)):
		span_size = end_ranges[i] - start_ranges[i] + 1 
		cur_words = words[start_ranges[i]:end_ranges[i]+1]
		cur_tags = tags[start_ranges[i]:end_ranges[i]+1]
		cur_heads = heads[start_ranges[i]:end_ranges[i]+1]
		cur_deps = deps[start_ranges[i]:end_ranges[i]+1]

		num_of_outward_heads = 0
		head_of_head_pos = 'ROOT'
		head_word = '_'

		# shifting heads
		for j in range(0,len(cur_heads)):
			shift = cur_heads[j] - start_ranges[i]
			if  shift <= 0 or shift>span_size:
				num_of_outward_heads+=1
				if shift != 0:
					head_of_head_pos = deps[start_ranges[i]+j]
				head_word = words[start_ranges[i]+j]
			if shift<=0:
				cur_heads[j] = '-1'
			elif shift>span_size:
				cur_heads[j] = str(span_size + 1)
			else:
				cur_heads[j] = str(shift)

		if num_of_outward_heads == 1:
			
			next_pos = '_' if end_ranges[i] == len(heads) -1 else tags[end_ranges[i]+1]
			prev_pos = '_' if start_ranges[i] ==  0 else tags[start_ranges[i]-1]
			output_list.append(prev_pos)
			output_list.append(next_pos)
			output_list.append(head_of_head_pos)
			output_list.append(head_word)
			output_list.append(' '.join(cur_words))
			output_list.append(' '.join(cur_tags))
			output_list.append(' '.join(cur_heads))
			output_list.append(' '.join(cur_deps))
			output_list.append('\n')
	if len(output_list)>0:
		return '\n'.join(output_list)
	else:
		return ''

def extract_possible_spans(file_path, output_path, span_min_length):
	reader = codecs.open(file_path,'r',encoding='utf-8')
	writer = codecs.open(output_path, 'w',encoding= 'utf-8')

	cnt = 1
	line = 'xxx'
	while line:
		words = reader.readline().strip().split()
		tags = reader.readline().strip().split()
		labels = reader.readline().strip().split()
		heads = map(int,reader.readline().strip().split())
		
		writer.write(get_spans_(words,tags,heads,labels, span_min_length))
		cnt+=1
		if cnt%1000==0:
			sys.stdout.write('%s\r' % (str(cnt)+'...'))

		line = reader.readline()
	sys.stdout.write('%s\r' % (str(cnt)+'...\n'))


def test_main():
	words = ['I', 'want','to','say','something','that','I','think','is','useful','.']
	tags = ['PRON', 'VERB','ADP','VERB','NOUN','CONJ','PRON','VERB','VERB','ADJ','.']
	heads = [2,0,-1,2,4,5,8,6,8,-1,8]
	labels = ['SUBJ', 'ROOT','ADP','VERB','NOUN','CONJ','PRON','VERB','VERB','ADJ','.']
	print get_spans_(words,tags,heads,labels, 3)

if __name__ == '__main__':
	extract_possible_spans(os.path.abspath(sys.argv[1]),os.path.abspath(sys.argv[2]), int(sys.argv[3]))
	#test_main()
