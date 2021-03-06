import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<3:
	print 'conll_folder conll_out_folder'
	sys.exit(0)
conll_folder = os.path.abspath(sys.argv[1])+'/'
eval_folder = os.path.abspath(sys.argv[2])+'/'

def eval_conll(parsed,gold):
	all_d = 0
	u_c = 0
	l_c = 0

	r1 = codecs.open(parsed,'r')
	r2 = codecs.open(gold,'r')
	line1 = r1.readline()
	while line1:
		line2 = r2.readline()

		spl1 = line1.strip().split('\t')
		spl2 = line2.strip().split('\t')
		if len(spl1)>5:
			if spl2[3]!='PUNCT':
				all_d+=1
				if spl1[6]==spl2[6]:
					u_c+=1
					if spl1[7]==spl2[7]:
						l_c+=1

		line1 = r1.readline()

	uas = 100 * float(u_c)/all_d
	las = 100 * float(l_c)/all_d

	return uas,las

output = list()
output.append('lang\tdata\tuas\tlas')

for f in sorted(os.listdir(eval_folder)):
	l = f
	if '_' in f:
		l = f[:f.rfind('_')]
	uas,las = eval_conll(eval_folder+f,conll_folder+f)
	
	#print l+'\t'+f+'\t'+str("{0:.2f}".format(uas))+'\t'+str("{0:.2f}".format(las))
	output.append(l+'\t'+f+'\t'+str("{0:.2f}".format(uas))+'\t'+str("{0:.2f}".format(las)))
		


#print '***************************************************************'
print '\n'.join(output)
