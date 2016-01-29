from collections import defaultdict    
from mst_dep_tree_loader import DependencyTree
import sys,codecs,os

def retrieveDeps(bd, s, t, direction, completeness, finalDeps):

    if s == t:
        return

    r = bd[s][t][direction][completeness]
    if completeness == 1:
        if direction == 0:
            retrieveDeps(bd, s, r, 0, 0, finalDeps)
            retrieveDeps(bd, r, t, 0, 1, finalDeps)
        else:
            retrieveDeps(bd, s, r, 1, 1, finalDeps)
            retrieveDeps(bd, r, t, 1, 0, finalDeps)
    else:
        if direction == 0:
            finalDeps[t] = s
            retrieveDeps(bd, s, r, 0, 1, finalDeps)
            retrieveDeps(bd, r + 1, t, 1, 1, finalDeps)
        else:
            finalDeps[s] = t
            retrieveDeps(bd, s, r, 0, 1, finalDeps)
            retrieveDeps(bd, r + 1, t, 1, 1, finalDeps)

def decode(l, dep_counts):
    scores = [[0 for i in range(l)] for j in range(l)]
    finalDeps = [0 for i in range(l)]
    finalDeps[0] = -1

    for i in range(l):
        for j in range(i+1,l):
            if dep_counts.has_key(i) and dep_counts[i].has_key(j):
                scores[i][j] = dep_counts[i][j]
            if dep_counts.has_key(j) and dep_counts[j].has_key(i):
                scores[j][i] =  dep_counts[j][i]
    #direction: 0=right, 1=left
    # completeness: 0=incomplete, 1=complete

    right = 0
    left = 1
    complete = 1
    incomplete = 0

    c  = [[[[0.0 for i in range(2)] for j in range(2)] for k in range(l)] for f in range(l)]
    bd  = [[[[0 for i in range(2)] for j in range(2)] for k in range(l)] for f in range(l)]

    for k in range(1,l):
        for s in range(0,l):
            t = s+ k
            if t >= l:
                break

            c[s][t][left][incomplete] = float('-inf')
            c[s][t][right][incomplete] = float('-inf')

            for r in range(s,t):
                bestRightScore = scores[s][t]
                bestLeftScore = scores[t][s]

                newLeftValue = c[s][r][right][complete] + c[r + 1][t][left][complete] + bestLeftScore
                if newLeftValue > c[s][t][left][incomplete]:
                    c[s][t][left][incomplete] = newLeftValue
                    bd[s][t][left][incomplete] = r

                newRightValue = c[s][r][right][complete] + c[r + 1][t][left][complete] + bestRightScore
                if newRightValue>=c[s][t][right][incomplete]:
                    c[s][t][right][incomplete] = newRightValue
                    bd[s][t][right][incomplete] = r

            c[s][t][left][complete] = float('-inf')
            c[s][t][right][complete] = float('-inf')
            for r in range(s,t+1):
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
    return finalDeps

trees= list()
print 'loading trees'
weights = list()
for i in range(1,len(sys.argv)-1):
    sys.stdout.write(str(i)+'...')
    trees.append(DependencyTree.load_trees_from_file(os.path.abspath(sys.argv[i])))
    #weights.append(float(sys.argv[i+1]))
sys.stdout.write('\n')
writer = codecs.open(os.path.abspath(sys.argv[-1]),'w')

print 'getting best trees'
for i in range(0, len(trees[0])):
    l = len(trees[0][i].words) + 1
    dep_counts = defaultdict()
    for j in range(0, l):
        dep_counts[j]=defaultdict(float)

    for j in range(0,len(trees)):
        weight = 1 #weights[j]
        for m in range(1,l):
            h = trees[j][i].heads[m-1]
            try:
                dep_counts[h][m] += weight
            except:
                print  trees[j][i].heads
                sys.exit(0)

    new_heads = decode(l, dep_counts)[1:]

    trees[0][i].heads = new_heads
    writer.write(trees[0][i].tree_str().strip()+'\n\n')

    if i%100==0:
        sys.stdout.write(str(i)+'...')
sys.stdout.write(str(i)+'\n')
writer.close()



