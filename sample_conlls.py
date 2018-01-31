import os,sys,codecs,random
from mst_dep_tree_loader import DependencyTree
from collections import defaultdict
from random import randint

if len(sys.argv)<4:
	print 'conll_file output_file max_num'
	sys.exit(0)


print 'reading trees'
t = DependencyTree.load_trees_from_conll_file(os.path.abspath(sys.argv[1]))

print 'writing trees'
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')
max_num = min(int(sys.argv[3]), len(t))

c = 0
seen = set()
v = 0
while True:
	i = random.randint(0,len(t)-1)
	v += 1
	if (not i in seen) and len(t[i].tags)>1: # and DependencyTree.is_projective(t[i].heads)
		seen.add(i)
		writer.write(t[i].conll_str()+'\n\n')
		c+= 1
		if c%1000==0:
			sys.stdout.write(str(c)+'...')
	if c>= max_num:
		break
sys.stdout.write(str(c)+'\n')
print v
writer.close()
