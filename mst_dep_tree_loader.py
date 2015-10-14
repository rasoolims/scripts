import codecs, os, sys
from collections import defaultdict
from extract_dependency_spans import SpanInfo

class DependencyTree:
	def __init__(self, words, tags, heads, labels):
		self.words = words
		self.tags = tags
		self.heads = heads
		self.labels = labels
		self.reverse_tree = defaultdict(set)

		self.index = dict()
		self.reverse_index = dict()
		for i in range(0,len(words)):
			self.index[i+1]=i+1
			self.reverse_index[i+1]=i+1

		# We need to increment index by one, because of the root.
		for i in range(0,len(heads)):
			self.reverse_tree[heads[i]].add(i+1)


	@staticmethod
	def load_tree_from_string(tree_str):
		spl = tree_str.strip().split('\n')
		words = spl[0].split()
		tags= spl[1].split()
		labels = spl[2].split()
		heads = [int(x) for x in spl[3].split()]
		return DependencyTree(words, tags, heads, labels)

	@staticmethod
	def load_trees_from_file(file_str):
		tree_list = list()
		[tree_list.append(DependencyTree.load_tree_from_string(tree_str)) for tree_str in codecs.open(file_str,'r').read().strip().split('\n\n')]
		return tree_list

	def get_span_list(self, head, span_set):
		span_set.add(head)
		if self.reverse_tree.has_key(head):
			for child in self.reverse_tree[head]:
				self.get_span_list(child,span_set)
		
	def reorder(self, head, order_set):
		node_set = set(self.reverse_tree[head])
		node_set.add(head)

		if len(node_set) != len(order_set):
			print ''
			print self.tree_str()
			print ''
			print head
			print order_set
			print node_set

		assert len(node_set) == len(order_set)

		node_set = sorted(node_set)

		new_words = list()
		new_tags = list()
		new_heads = list()
		new_labels = list()
		new_index = dict()

		left_words =list()
		right_words = list()
		new_ordering = list()
		for i in range(0,len(order_set)):
			node = node_set[order_set[i]] 
			if node == head:
				new_ordering.append(head)
			else:
				span_set = set()
				self.get_span_list(node, span_set)
				for i in sorted(span_set):
					new_ordering.append(i)

		for i in range(1,len(self.words)+1):
			if not i in new_ordering:
				if i<head:
					left_words.append(i)
				else:
					right_words.append(i)

		new_ordering = left_words + new_ordering + right_words

		ordering_index = dict()
		cnt = 0
		for i in new_ordering:
			new_words.append(self.words[i-1])
			new_tags.append(self.tags[i-1])
			new_labels.append(self.labels[i-1])
			cnt+=1
			new_index[cnt] = self.index[i]
			ordering_index[i] = cnt

		for i in new_ordering:
			if self.heads[i-1] == 0:
				new_heads.append(0)
			else:
				h = self.heads[i-1]
				new_heads.append(ordering_index[h])

		new_tree = DependencyTree(new_words,new_tags, new_heads, new_labels)
		new_tree.index = new_index

		rev_index = dict()
		for i in new_index.keys():
			rev_index[new_index[i]]=i

		new_tree.reverse_index = rev_index

		return new_tree

	def flip_head(self, h, m):
		if self.heads[m-1] != h:
			return

		self.heads[m-1] = self.heads[h-1]
		self.heads[h-1] = m
		tmp = self.labels[m-1]
		self.labels[m-1] = self.labels[h-1]
		self.labels[h-1] = tmp

		for k in range(0,len(self.heads)):
			if k+1 == m and k+1 == h:
				continue

			if self.heads[k] == h:
				self.heads[k] = m

	def flip_copula_head(self, h, m):
		self.flip_head(h,m)
		self.labels[h-1] = 'attr'

	def tree_str(self):
		lst = list()
		lst.append('\t'.join(self.words))
		lst.append('\t'.join(self.tags))
		lst.append('\t'.join(self.labels))
		lst.append('\t'.join(str(x) for x in self.heads))
		return '\n'.join(lst)

	def expand_tree(self, span_info, word_index):
		new_words = list()
		new_tags = list()
		new_heads = list()
		new_deps = list()

		for i in range(0,word_index+1):
			new_words.append(self.words[i])
			new_tags.append(self.tags[i])
			new_deps.append(self.labels[i])
			head = self.heads[i] if self.heads[i]<= (word_index+1) else self.heads[i] + len(span_info.words)
			new_heads.append(head)
		for i in range(0, len(span_info.words)):
			if i==0:
				span_info.words[i]= span_info.words[i].lower()
			new_words.append(span_info.words[i])
			new_tags.append(span_info.tags[i])
			dep = span_info.head_dependency if span_info.heads[i] < 0 else span_info.labels[i]
			new_deps.append(dep)
			head = word_index if span_info.heads[i] < 0 else span_info.heads[i] + word_index + 1
			new_heads.append(head)
		for i in range(word_index+1,len(self.words)):
			new_words.append(self.words[i])
			new_tags.append(self.tags[i])
			new_deps.append(self.labels[i])
			head = self.heads[i] if self.heads[i]<= (word_index+1) else self.heads[i] + len(span_info.words)
			new_heads.append(head)

		return DependencyTree(new_words,new_tags,new_heads,new_deps)



	def extend_tree_inclusive(self, span_info, word_index):
		new_words = list()
		new_tags = list()
		new_heads = list()
		new_deps = list()
		new_word_index = word_index + 1
		assert span_info.head_word == self.words[word_index] and span_info.head_dependency == self.labels[word_index]
		for i in range(0,word_index):
			new_words.append(self.words[i])
			new_tags.append(self.tags[i])
			new_deps.append(self.labels[i])
			head = self.heads[i] if self.heads[i]<= word_index else self.heads[i] + len(span_info.words) - 1
			if (self.heads[i] == word_index + 1) and not span_info.is_left_head:
				head = self.heads[i]
			new_heads.append(head)
		for i in range(0, len(span_info.words)):
			if i==0 and word_index!=0:
				span_info.words[i]=span_info.words[i].lower()
			new_words.append(span_info.words[i])
			new_tags.append(span_info.tags[i])
			dep = span_info.head_dependency if span_info.heads[i] < 0 else span_info.labels[i]
			new_deps.append(dep)
			head = span_info.heads[i] + word_index
			if span_info.heads[i] < 0:
				new_word_index += i
				if self.heads[word_index]>word_index:
					head = self.heads[word_index] + len(span_info.words) - 1
				else:
					head = self.heads[word_index]
			new_heads.append(head)


		for i in range(word_index+1,len(self.words)):
			new_words.append(self.words[i])
			new_tags.append(self.tags[i])
			new_deps.append(self.labels[i])
			head = self.heads[i] if self.heads[i]<= word_index else self.heads[i] + len(span_info.words)-1
			if self.heads[i] == word_index + 1:
				head = new_word_index
			new_heads.append(head)

		return DependencyTree(new_words,new_tags,new_heads,new_deps)

if __name__ == '__main__':
	words = ['I', 'want','to','say','something','that','I','think','is','useful','.']
	tags = ['PRON', 'VERB','ADP','VERB','NOUN','CONJ','PRON','VERB','VERB','ADJ','.']
	heads = [2,0,4,2,4,5,8,6,8,9,2]
	labels = ['SUBJ', 'ROOT','ADP','VERB','NOUN','CONJ','PRON','VERB','VERB','ADJ','.']
	tree = DependencyTree(words,tags,heads,labels)
	print tree.words
	print tree.heads
	print '***************'

	new_words = ['very', 'useful']
	new_tags = ['v','u']
	new_deps = [1,-1]
	new_labels = ['old_dep', 'new_dep']
	span_info = SpanInfo(True, 'useful', 'NOUN','CONJ','NOUN', 'new_dep',new_words,new_tags,new_deps,new_labels)

	new_tree = tree.expand_tree(span_info,4)
	print new_tree.words
	print new_tree.tags
	print new_tree.labels
	print new_tree.heads
	print '***************'

	new_words = ['Kindly','something','very', 'useful']
	new_tags = ['k','s','v','u']
	new_deps = [2,-1,4,2]
	new_labels = ['K','NOUN','old_dep', 'new_dep']
	span_info = SpanInfo(True, 'something', 'NOUN','CONJ','NOUN', 'NOUN',new_words,new_tags,new_deps,new_labels)

	new_tree = tree.extend_tree_inclusive(span_info,4)
	print new_tree.words
	print new_tree.tags
	print new_tree.labels
	print new_tree.heads
	print '***************'

	heads = [2,0,4,2,8,5,8,6,8,9,2]
	tree = DependencyTree(words,tags,heads,labels)
	new_tree = tree.extend_tree_inclusive(span_info,4)
	print new_tree.words
	print new_tree.tags
	print new_tree.labels
	print new_tree.heads
	print '***************'

	words = ['1','2','3','4','5','6','7','8','9','10']
	tags =  ['1','2','3','4','5','6','7','8','9','10']
	labels = ['1','2','3','4','5','6','7','8','9','10']
	heads = [2,0,5,3,2,2,8,9,6,2]
	tree = DependencyTree(words,tags,heads,labels)
	print tree.tree_str()
	print '***************'
	
	new_tree = tree.reorder(2,[2,3,0,1,4])
	print new_tree.tree_str()
	print new_tree.index
	print new_tree.reverse_index

	print '***************'

	newer_tree = new_tree.reorder(4,[1,0])
	print newer_tree.tree_str()
	print newer_tree.index
	print newer_tree.reverse_index

	print '***************'

	newer_tree2 = newer_tree.reorder(3,[0,1])
	print newer_tree2.tree_str()
	print newer_tree2.index
	print newer_tree2.reverse_index
