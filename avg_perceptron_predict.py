import os,sys,math,operator,codecs,traceback
from collections import defaultdict
from avg_perceptron import avg_perceptron

test_path=os.path.abspath(sys.argv[1])
model_path=os.path.abspath(sys.argv[2])
iter_num=int(sys.argv[3])
output=codecs.open(os.path.abspath(sys.argv[4]),'w')

dap=avg_perceptron(model_path+'.model_'+str(iter_num),model_path+'.lab')


test_reader=codecs.open(test_path,'r')
line=test_reader.readline()

all_lab=0
cnt=0
correct=0

true_positive = defaultdict(int)
false_positive = defaultdict(int)
false_negative = defaultdict(int)

while line:
	flds=line.strip().split('\t')
	argmax=''

	if len(flds)>1:
		cnt+=1
		if cnt%1000==0:
			sys.stdout.write(str(cnt)+'...')
			sys.stdout.flush()

		label=flds[-1]
		feats=flds[:-1]

		argmax=dap.argmax(feats,True)
		all_lab+=1
		if argmax==label:
			correct+=1
			true_positive[label]+=1
		else:
			false_positive[label]+=1
			false_negative[argmax]+=1
	
	output.write(argmax+'\n')
	line=test_reader.readline()

output.flush()
output.close()

for label in dap.labels:
	prec_denom = true_positive[label] + false_positive[label]
	recall_denom = true_positive[label] + false_negative[label]

	if prec_denom== 0 and recall_denom ==0:
		continue

	precision = 0 if prec_denom == 0 else float(true_positive[label])/prec_denom
	recall = 0 if recall_denom == 0 else float(true_positive[label])/recall_denom
	f_score = 0 if (precision==0 or recall==0) else (2*recall*precision)/(recall+precision)
	sys.stdout.write(label+'\t'+str(recall_denom)+'\t'+str("%.2f" % round(precision,2))+'\t'+str("%.2f" % round(recall,2))+'\t'+str("%.2f" % round(f_score,2))+'\n')



accuracy=100.0*float(correct)/cnt
sys.stdout.write('\naccuracy: '+str(accuracy)+'\n')
