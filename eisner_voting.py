import sys,codecs,os
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict

def retrieveDeps(bd, s, t, direction, completeness, finalDeps):
	if s == t:
		return 

	r = bd[s][t][direction][completeness]
	if completeness == 1:
		if direction ==0:
			retrieveDeps(bd, s, r, 0, 0, finalDeps)
			retrieveDeps(bd, r, t, 0, 1, finalDeps)
		else:
			retrieveDeps(bd, s, r, 1, 1, finalDeps)
			retrieveDeps(bd, r, t, 1, 0, finalDeps)
	else:
		if direction ==0:
			finalDeps[t] = s
			retrieveDeps(bd, s, r, 0, 1, finalDeps)
			retrieveDeps(bd, r + 1, t, 1, 1, finalDeps)
		else:
			finalDeps[s] = t
			retrieveDeps(bd, s, r, 0, 1, finalDeps)
			retrieveDeps(bd, r + 1, t, 1, 1, finalDeps)

def eisner1stOrder(l, labels, weights):
	scores = [[0 for i in range(l)] for j in range(l)]
	best_labels = [['_' for i in range(l)] for j in range(l)]
	finalDeps = [0 for i in range(l)]
	finalDeps[0] = -1
	for i in range(0,l):
		for j in range(i+1,l):
			scores[i][j] = float('-inf')
			scores[j][i] = float('-inf')

			for label in labels:
				s1 = weights[i][j][label]
				if s1 > scores[i][j]:
					scores[i][j] = s1
					best_labels[i][j] = label
				
				s2 = weights[j][i][label]
				if s2 > scores[j][i]:
					scores[j][i] = s2
					best_labels[j][i] = label
	right = 0;
	left = 1;
	complete = 1;
	incomplete = 0;
	c  = [[[[0.0 for i in range(2)] for j in range(2)] for k in range(l)] for f in range(l)]
	bd  = [[[[0 for i in range(2)] for j in range(2)] for k in range(l)] for f in range(l)]

	for s in range(0,l):
		c[s][s][right][complete] = 0.0
		c[s][s][left][complete] = 0.0

	for k in range(1,l):
		for s in range(0,l):
			t = s+k
			if t>=l:
				break

			# create incomplete items
			c[s][t][left][incomplete] = float('-inf')
			c[s][t][right][incomplete] = float('-inf')

			for r in range(s,t):
				bestRightScore = scores[s][t]
				bestLeftScore = scores[t][s]

				newLeftValue = c[s][r][right][complete] + c[r + 1][t][left][complete] + bestLeftScore;
				if newLeftValue > c[s][t][left][incomplete]:
					c[s][t][left][incomplete] = newLeftValue
					bd[s][t][left][incomplete] = r;

				newRightValue = c[s][r][right][complete] + c[r + 1][t][left][complete] + bestRightScore;
				if newRightValue > c[s][t][right][incomplete]:
					c[s][t][right][incomplete] = newRightValue
					bd[s][t][right][incomplete] = r

			# create complete spans
			c[s][t][left][complete] = float('-inf')
			c[s][t][right][complete] = float('-inf')
			for  r in range(s,t+1):
				if r<t:
					newLeftScore = c[s][r][left][complete] + c[r][t][left][incomplete]
					if newLeftScore > c[s][t][left][complete]:
						c[s][t][left][complete] = newLeftScore
						bd[s][t][left][complete] = r

				if r>s:
					newRightScore = c[s][r][right][incomplete] + c[r][t][right][complete]
					if newRightScore > c[s][t][right][complete]:
						c[s][t][right][complete] = newRightScore
						bd[s][t][right][complete] = r

	retrieveDeps(bd, 0, l - 1, 0, 1, finalDeps)
	final_labels =list()
	for i in range(0, len(finalDeps)):
		if finalDeps[i]==-1:
			final_labels.append("_")
		else:
			final_labels.append(best_labels[finalDeps[i]][i])


	for i in range(0,len(finalDeps)):
		h = finalDeps[i]
		l = final_labels[i]
		if h>=0:
			if weights[h][i][l] < 1:
				finalDeps[i] = -1
				final_labels[i] = '_'
	return final_labels, finalDeps


#########################################################################################################
labels = set()
print 'loading trees'
weights = list()
tree_set = defaultdict(list)
for i in range(1,len(sys.argv)-1):
	sys.stdout.write(str(i)+'...')
	tree_s = DependencyTree.load_trees_from_file(os.path.abspath(sys.argv[i]))
	for t in tree_s:
		for i in range(1,len(t.words)+1):
			labels.add(t.labels[i-1])
		sen = ' '.join(t.words)
		tree_set[sen].append(t)
	#weights.append(float(sys.argv[i+1]))
sys.stdout.write('\n')
writer = codecs.open(os.path.abspath(sys.argv[-1]),'w')

print 'getting best trees'
cnt = 0 
for sen in tree_set.keys():
	l = len(tree_set[sen][0].words) + 1
    
	weights = dict()
	for h in range(0,l+1):
		weights[h] = dict()
		for d in range(0,l+1):
			weights[h][d] = dict()
			for label in labels:
				weights[h][d][label] = 0

	
	for tree in tree_set[sen]:
		for m in range(1,l):
			h = tree.heads[m-1]
			label = tree.labels[m-1]
			if h>=0:
			 	weights[h][m][label] += 1

	labs, finalDeps = eisner1stOrder(l, labels, weights)

	tree = tree_set[sen][0]

	tree.heads = finalDeps[1:]
	tree.labels = labs[1:]

	writer.write(tree.tree_str().strip()+'\n\n')

	cnt +=1
	if cnt%100==0:
		sys.stdout.write(str(cnt)+'...')
sys.stdout.write(str(cnt)+'\n')
writer.close()




