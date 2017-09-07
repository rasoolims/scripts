import os,sys,operator
from collections import defaultdict

sup_sens = open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n\n')
proj_sens = open(os.path.abspath(sys.argv[2]),'r').read().strip().split('\n\n')

l = len(proj_sens)
assert l==len(sup_sens)

def density(lines):
	p = 0
	for line in lines:
		projection = line.strip().split('\t')[12]
		if projection!='?': p+=1
	d = float(p)/len(lines)

	if d<=0.4: return 1
	if d>0.4 and d<=0.6: return 2
	if d>0.6 and d<=0.8: return 3
	if d>0.8: return 4


proj_levels = defaultdict(int)

for i in xrange(l):
	spl_proj = proj_sens[i].strip().split('\n')
	spl_sup = sup_sens[i].strip().split('\n')
	proj_levels[density(spl_proj)]+=1
print proj_levels
