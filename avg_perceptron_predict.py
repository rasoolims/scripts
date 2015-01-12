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

while line:
	flds=line.strip().split('\t')
	argmax=''

	if len(flds)>1:
		cnt+=1
		if cnt%100000==0:
			sys.stdout.write(str(cnt)+'...')
			sys.stdout.flush()

		label=flds[-1]
		feats=flds[:-1]

		argmax=dap.argmax(feats,True)
		all_lab+=1
		if argmax==label:
			correct+=1
	
	output.write(argmax+'\n')
	line=test_reader.readline()

output.flush()
output.close()

accuracy=100.0*float(correct)/cnt
sys.stdout.write('\naccuracy: '+str(accuracy)+'\n')
