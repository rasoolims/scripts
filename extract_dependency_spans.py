#! /usr/bin/python

import codecs, os, pickle, sys
from collections import defaultdict

class SpanInfo:
	def __init__(self, is_left_head, head_word, prev_pos, next_pos, head_of_head_pos, head_dependency, words, tags, heads, labels):
		self.is_left_head = is_left_head
		self.head_word = head_word
		self.prev_pos = prev_pos
		self.next_pos = next_pos
		self.head_of_head_pos = head_of_head_pos
		self.head_dependency = head_dependency
		self.words = words
		self.tags = tags
		self.heads = [int(x) for x in heads]
		self.labels = labels

	@staticmethod
	def get_span_from_str(str_info):
		spl = str_info.strip().split('\n')
		is_left_head = bool(spl[0])
		head_word = spl[1]
		prev_pos = spl[2]
		next_pos = spl[3]
		head_of_head_pos = spl[4]
		head_dependency = spl[5]
		words = spl[6].split(' ')
		tags = spl[7].split(' ')
		heads = [int(x) for x in spl[8].split(' ')]
		labels = spl[9].split(' ')
		return SpanInfo(is_left_head,head_word, prev_pos, next_pos, head_of_head_pos, head_dependency, words, tags, heads, labels)

class SpanDicts:
	def __init__(self):
		self.span_info_dic = defaultdict(SpanInfo)
		self.head_word_info = defaultdict(list)
		self.prev_pos_info = defaultdict(list)
		self.next_pos_info = defaultdict(list)
		self.context_pos_info = defaultdict(list)
		self.context_dep_pos_info = defaultdict(list)
		self.context_dep_head_pos_info = defaultdict(list)
		self.head_word_dep_info = defaultdict(list)
		self.head_of_head_pos_info = defaultdict(list)

	def add_span_info(self, span, span_id):
		self.span_info_dic[span_id] = span
		self.head_word_info[span.head_word].append(span_id)
		self.prev_pos_info[span.prev_pos].append(span_id)
		self.next_pos_info[span.next_pos].append(span_id)
		self.context_pos_info[span.prev_pos +' ' + span.next_pos].append(span_id)
		self.head_word_dep_info[span.head_word +' ' + span.head_dependency].append(span_id)
		self.context_dep_pos_info[span.prev_pos +' ' + span.next_pos + ' ' + span.head_dependency].append(span_id)
		self.head_of_head_pos_info[span.head_of_head_pos].append(span_id)
		self.context_dep_head_pos_info[span.prev_pos +' ' + span.next_pos + ' ' + span.head_dependency + ' '+ span.head_of_head_pos].append(span_id)


	@staticmethod
	def save_to_file(span_dict, output_path):
		pickle.dump(span_dict, open(output_path,'wb'))

	@staticmethod
	def load_from_file(input_file):
		return pickle.load(open(input_file,'rb'))

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
		head_dependency = 'ROOT'
		is_left_head = False

		# shifting heads
		for j in range(0,len(cur_heads)):
			shift = cur_heads[j] - start_ranges[i]
			if  shift <= 0 or shift>span_size:
				num_of_outward_heads+=1
				if shift != 0:
					head_of_head_pos = tags[start_ranges[i]+j]
				head_word = words[start_ranges[i]+j]
				head_dependency = deps[start_ranges[i]+j]
			if shift<=0:
				cur_heads[j] = '-1'
				is_left_head = True
			elif shift>span_size:
				cur_heads[j] = '-1'
			else:
				cur_heads[j] = str(shift)

		if num_of_outward_heads == 1:
			next_pos = '_' if end_ranges[i] == len(heads) -1 else tags[end_ranges[i]+1]
			prev_pos = '_' if start_ranges[i] ==  0 else tags[start_ranges[i]-1]
			output_list.append(str(is_left_head))
			output_list.append(head_word)
			output_list.append(prev_pos)
			output_list.append(next_pos)
			output_list.append(head_of_head_pos)
			output_list.append(head_dependency)
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
	span_dic = SpanDicts()

	cnt = 1
	line = 'xxx'
	while line:
		words = reader.readline().strip().split()
		tags = reader.readline().strip().split()
		labels = reader.readline().strip().split()
		heads = map(int,reader.readline().strip().split())
		
		spans = get_spans_(words,tags,heads,labels, span_min_length).split('\n\n')
		for span in spans:
			if not span.strip():
				continue
			span_dic.add_span_info(SpanInfo.get_span_from_str(span), cnt)
			cnt+=1
			if cnt%1000==0:
				sys.stdout.write('%s\r' % (str(cnt)+'...'))

		line = reader.readline()
	sys.stdout.write('%s\r' % (str(cnt)+'...\n'))

	sys.stdout.write('%s\r' % 'dumping span info into a file ...\n')
	SpanDicts.save_to_file(span_dic,output_path)


if __name__ == '__main__':
	if len(sys.argv)<4:
		print 'args: [input mst path] [output span file] [min span length]'
		sys.exit(0)
	extract_possible_spans(os.path.abspath(sys.argv[1]),os.path.abspath(sys.argv[2]), int(sys.argv[3]))
