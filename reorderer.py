import os,sys,codecs,random,operator,math
from mst_dep_tree_loader import DependencyTree
from languagemodel import LanguageModel

class Reorderer:
	
	def __init__(self, src_lm_path, dst_lm_path, a1, a2, a3):
	#def __init__(self, src_lm_path):
		self.src_lm = LanguageModel(src_lm_path)
		self.dst_lm = LanguageModel(dst_lm_path)
		self.a1 = a1
		self.a2 = a2
		self.a3 = a3

		self.permutation_set = list()
		for l in range(1,100):
			self.permutation_set.append(Reorderer.get_permutation_set(l+1))

		print 'init'

	def score(self, tree):
		distance = tree.index[1] - 1
		for i in range(2, len(tree.words)+1):
			distance += abs(tree.index[i] - tree.index[i-1]) - 1
			distance+= abs(i-1 - tree.reverse_index[i-1])
		distance += abs(len(tree.words)+1 - tree.index[len(tree.words)]) - 1

		words = ['<s>','<s>','<s>','<s>']+tree.tags +['</s>']

		l1 = self.dst_lm.score_arr(words)
		l2 = self.src_lm.score_arr(words)

		sc = (self.a1*l1+self.a2*l2-self.a3*distance)
		#print ' '.join(tree.tags)
		#print sc
		#print ''
		return sc 

	@staticmethod
	def get_permutation_set(l):
		orig_order = list()
		for i in range(0,l):
			orig_order.append(i)

		max_num = 100 if len(orig_order)>=5 else (24 if len(orig_order)==4 else (6 if len(orig_order)==3 else 2))
		final_set = set()
		new_set_str = ' '.join(str(x) for x in orig_order) 
		final_set.add(new_set_str)

		added = 0
		while added < max_num-1:
			left_set = list(orig_order)
			new_set = list()
			for j in range(0,len(orig_order)):
				random_index = random.randrange(0,len(left_set))
				new_set.append(left_set[random_index])
				del left_set[random_index]

			new_set_str = ' '.join(str(x) for x in new_set) 
			if not new_set_str in final_set:
				final_set.add(new_set_str)
				added+=1

		return final_set

	def reorder_tree(self, tree, beam_size):
		head = -1
		for h in tree.reverse_tree[0]:
			head = h
			break
		head_children = tree.reverse_tree[head]

		to_visit = list()
		to_visit.append(head)

		current_beam = [tree]

		best_tree = tree

		while len(to_visit)>0:
			n = to_visit.pop(0)
			if tree.reverse_tree.has_key(n) and len(tree.reverse_tree[n])>0:
				for c in tree.reverse_tree[n]:
					to_visit.append(c)
			else:
				continue

			#print 'head-->',n

			new_beam = dict()

			permutation = self.permutation_set[len(tree.reverse_tree[n])-1]

			for p in permutation:
				order = [int(x) for x in p.split(' ')]
				for t in current_beam:
					c_n = t.reverse_index[n]

					if len(tree.reverse_tree[n])>100:
						print ''
						print tree.tree_str()
						print '------'

					new_tree = t.reorder(c_n, order)
					new_beam[new_tree] = self.score(new_tree)

			cnt = 0
			pruned_beam = list()
			for it in sorted(new_beam.items(), key=operator.itemgetter(1), reverse=True):
				cnt+=1

				best_tree = it[0]

				pruned_beam.append(it[0])
				if cnt>= beam_size:
					break
			current_beam = pruned_beam
		return best_tree

	@staticmethod
	def test():
		words = ['1','2','3','4','5','6','7','8','9','10']
		tags =  ['DET','ADJ','NOUN','VERB','DET','ADJ','ADJ','NOUN','NOUN','.']
		labels = ['1','2','3','4','5','6','7','8','9','10']
		heads = [3,3,4,0,9,9,9,9,4,4]
		tree = DependencyTree(words,tags,heads,labels)
		
		print tree.tree_str()
		print ',,,,,,,'
		reorderer = Reorderer('/tmp/en.lm','/tmp/de.lm',1,0.,0)
		best_tree = reorderer.reorder_tree(tree, 100)
		print best_tree.tree_str()

if __name__ =='__main__':
	if len(sys.argv)<3:
		Reorderer.test()
		sys.exit(0)

	src_lm_path = os.path.abspath(sys.argv[1])
	dst_lm_path = os.path.abspath(sys.argv[2])
	a1 = float(sys.argv[3])
	a2 = float(sys.argv[4])
	a3 = float(sys.argv[5])

	reorderer = Reorderer(src_lm_path,dst_lm_path,a1,a2,a3)
	trees = DependencyTree.load_trees_from_file(os.path.abspath(sys.argv[6]))
	writer = codecs.open(os.path.abspath(sys.argv[7]),'w')

	cnt = 0
	for tree in trees:
		writer.write(reorderer.reorder_tree(tree, 1).tree_str()+'\n\n')
		cnt+=1
		sys.stdout.write(str(cnt)+'...')
	writer.close()
sys.stdout.write('done!\n')