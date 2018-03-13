import codecs, os, sys
from collections import defaultdict
from extract_dependency_spans import SpanInfo

class DependencyTree:
	def __init__(self, words, tags, heads, labels):
		self.words = words
		self.lemmas = words
		self.tags = tags
		self.ftags = tags
		self.heads = heads
		self.labels = labels
		self.reverse_tree = defaultdict(set)
		self.lang_id = ''
		self.weight = 1.0

		self.index = dict()
		self.reverse_index = dict()
		for i in range(0,len(words)):
			self.index[i+1]=i+1
			self.reverse_index[i+1]=i+1

		# We need to increment index by one, because of the root.
		for i in range(0,len(heads)):
			self.reverse_tree[heads[i]].add(i+1)

	def __eq__(self, other):
		if isinstance(other, DependencyTree):
			return self.tree_str() == other.tree_str()
		return False

	def __ne__(self, other):
		return self.__eq__(other)

	def __hash__(self):
		return hash(self.tree_str())

	@staticmethod
	def trav(rev_head,h,visited):
		if rev_head.has_key(h):
			for d in rev_head[h]:
				if d in visited:
					return True
				visited.append(d)
				DependencyTree.trav(rev_head,d,visited)
		return False

	@staticmethod
	def is_full(heads):
		for dep1 in range(1,len(heads)+1):
			head1=heads[dep1-1]
			if head1<0:
				return False
		return True

	@staticmethod
	def is_nonprojective_arc(d1,h1,d2,h2):
		if d1 > h1 and h1 != h2:
			if (d1 > h2 and d1 < d2 and h1 < h2) or (d1 < h2 and d1 > d2 and h1 < d2):
				return True
		if d1 < h1 and h1 != h2:
			if (h1 > h2 and h1 < d2 and d1 < h2) or (h1 < h2 and h1 > d2 and d1 < d2):
				return True
		return False

	@staticmethod
	def get_nonprojective_arcs(heads):
		non_projectives = set()
		for i in xrange(len(heads)):
			if i in non_projectives:
				continue
			dep1,head1 = i+1,heads[i]
			for j in xrange(len(heads)):
				if i==j: continue
				dep2,head2 = j+1, heads[j]
				if DependencyTree.is_nonprojective_arc(dep1, head1, dep2, head2):
					non_projectives.add(i+1)
					non_projectives.add(j+1)
		return non_projectives

	@staticmethod
	def is_projective(heads):
		rev_head=defaultdict(list)
		for dep1 in range(1,len(heads)+1):
			head1=heads[dep1-1]
			if head1>=0:
				rev_head[head1].append(dep1)

		visited=list()
		#print rev_head
		if DependencyTree.trav(rev_head,0,visited):
			return False
		if len(visited)<len(heads) and DependencyTree.is_full(heads):
			return False

		rootN=0
		for dep1 in range(1,len(heads)+1):
			head1=heads[dep1-1]
			if head1==0:
				rootN+=1
			if rev_head.has_key(dep1):
				for d2 in rev_head[dep1]:
					if (d2<head1 and head1<dep1) or (d2>head1 and head1>dep1) and head1>0:
						return False

			for dep2 in range(1,len(heads)+1):
				head2=heads[dep2-1]
				if head1==-1 or head2==-1:
					continue
				if dep1>head1 and head1!=head2:
					if dep1>head2 and dep1<dep2 and head1<head2:
						return False
					if dep1<head2 and dep1>dep2 and head1<dep2:
						return False
				if dep1<head1 and head1!=head2:
					if head1>head2 and head1<dep2 and dep1<head2:
						return False
					if head1<head2 and head1>dep2 and dep1<dep2:
						return False
		if rootN<1:
			return False
		return True

	@staticmethod
	def load_tree_from_string(tree_str):
		spl = tree_str.strip().split('\n')
		words = spl[0].split()
		tags= spl[1].split()
		labels = spl[2].split()
		heads = [int(x) for x in spl[3].split()]
		return DependencyTree(words, tags, heads, labels)

	@staticmethod
	def load_tree_from_conll_string(tree_str):
		lines = tree_str.strip().split('\n')
		words = list()
		tags = list()
		heads = list()
		labels = list()
		lemmas = list()
		ftags = list()

		l_id = ''
		w = 1
		for line in lines:
			spl = line.split('\t')
			words.append(spl[1])
			lemmas.append(spl[2])
			tags.append(spl[3])
			ftags.append(spl[4])
			heads.append(int(spl[6]))
			l_id = spl[5]
			labels.append(spl[7])
			try:
				w = float(spl[8])
			except:
				w = 1

		tree = DependencyTree(words, tags, heads, labels)
		tree.lang_id = l_id
		tree.lemmas = lemmas
		tree.ftags = ftags
		tree.weight = w
		return tree

	@staticmethod
	def load_trees_from_file(file_str):
		tree_list = list()
		[tree_list.append(DependencyTree.load_tree_from_string(tree_str)) for tree_str in codecs.open(file_str,'r').read().strip().split('\n\n')]
		return tree_list

	@staticmethod
	def load_trees_from_conll_file(file_str):
		tree_list = list()
		[tree_list.append(DependencyTree.load_tree_from_conll_string(tree_str)) for tree_str in codecs.open(file_str,'r').read().strip().split('\n\n')]
		return tree_list

	def reorder_with_order(self, new_order):
		new_words, new_lemmas, new_tags, new_heads, new_labels = [], [], [], [], []
		rev_order = {0:0, -1:-1}
		for i, o in enumerate(new_order):
			new_words.append(self.words[o-1])
			new_lemmas.append(self.lemmas[o - 1])
			new_tags.append(self.tags[o - 1])
			new_labels.append(self.labels[o - 1])
			rev_order[o] = i + 1

		for o in new_order:
			new_head = rev_order[self.heads[o-1]]
			new_heads.append(new_head)

		tree = DependencyTree(new_words, new_tags, new_heads, new_labels)
		tree.lang_id = self.lang_id
		return tree


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

	def conll_str(self):
		lst = list()

		for i in range(0,len(self.words)):
			ln =str(i+1) +'\t'+self.words[i]+'\t'+self.lemmas[i]+'\t'+self.tags[i]+'\t'+self.ftags[i]+'\t'+self.lang_id+'\t'+str(self.heads[i])+'\t'+self.labels[i]+'\t'+str(self.weight)+'\t_'
			lst.append(ln)
		return '\n'.join(lst)

	# Uses ftag as chunk tag.
	def chunk_str(self):
		lst = list()

		for i in xrange(len(self.words)):
			ln = self.words[i].replace(' ','_')+' '+self.tags[i]+' '+self.ftags[i]
			lst.append(ln)
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
