# coding: utf8
import os,sys,codecs
from collections import defaultdict
from mst_dep_tree_loader import DependencyTree

def show_help():
	print 'python extract_trees.py [min_len] [min_proportion] [input_data] [output_data] [tree_max_len] partial(only_partial:optional)'

def trav(rev_head,h,visited):
	if rev_head.has_key(h):
		for d in rev_head[h]:
			if d in visited:
				return True
			visited.append(d)
			trav(rev_head,d,visited)
	return False

def has_proportion(heads,min_proportion):
	num=0
	for dep1 in range(1,len(heads)+1):
		if heads[dep1-1]>=0:
			num+=1
	prop=0
	try:
		prop=1.0/(len(heads))
	except:
		prop=0
	if min_proportion<=prop:
		return True
	return False

def extract_subtree(heads,min_len):
	'''
		extracts indices of words that should be included in the subtree
	'''
	start_index=1
	current_index=1

	spans=set()
	for i in range(1,len(heads)+1):
		for j in range(i+min_len,len(heads)+1):
			use_span=True
			num_of_outs=0
			for k in range(i,j+1):
				if heads[k-1]==-1:
					use_span=False
					break
				if heads[k-1]<i or heads[k-1]>j:
					num_of_outs+=1
				if num_of_outs>1:
					use_span=False
					break
			if use_span:
				for k in range(i,j+1):
					spans.add(k)

	final_heads=list()
	for i in range(1,len(heads)+1):
		head=heads[i-1] if i in spans else -1
		final_heads.append(head)

	return final_heads

def extract_full_trees(input_path,output_path,min_len,min_proportion, tree_max_len, only_partial):
	all_trees = DependencyTree.load_trees_from_conll_file(os.path.abspath(input_path))
	trees=defaultdict()
	writer=codecs.open(output_path,'w')

	for i in range(len(all_trees)):
		tree = all_trees[i]
		if len(tree.heads)>tree_max_len:
			continue

		if DependencyTree.is_projective(tree.heads):
			if DependencyTree.is_full(tree.heads) or has_proportion(tree.heads, min_proportion):
				if not only_partial:
					writer.write(tree.conll_str()+'\n\n')
			elif min_len<=len(tree.heads):
				new_heads=extract_subtree(tree.heads,min_len)
				has_subtree=False
				
				for h in new_heads:
					if h!=-1:
						has_subtree=True
						break
				if has_subtree:
					writer.write(tree.conll_str()+'\n\n')
		if i%1000==0:
			sys.stdout.write(str(i)+'...')
	writer.flush()
	writer.close()
	sys.stdout.write('\n')
	sys.stdout.flush()

if __name__ == '__main__':
	if len(sys.argv)<6:
		show_help()
		sys.exit(0)
	min_len=int(sys.argv[1])
	min_proportion=float(sys.argv[2])
	input_path=os.path.abspath(sys.argv[3])
	output_path=os.path.abspath(sys.argv[4])
	tree_max_len=int(sys.argv[5])
	only_partial = False
	if len(sys.argv)>6 and sys.argv[6]=='partial':
		only_partial = True

	extract_full_trees(input_path,output_path,min_len,min_proportion,tree_max_len, only_partial)