import os,sys,math,operator,codecs,traceback
from collections import defaultdict
from bin_avg_perceptron import bin_avg_perceptron

if __name__=='__main__':
	if len(sys.argv)<5:
		print 'python bin_avg_perceptron_predict.py [model_path] [iter_num] [threshold(optional; default:0)] [dev_path]'
		sys.exit(0)

	beta=0
	bias=0
	if len(sys.argv)>3:
		beta=float(sys.argv[3])
	model_path=os.path.abspath(sys.argv[1])
	iteration=int(sys.argv[2])
	dev_path=os.path.abspath(sys.argv[4])

	
	print 'threshold',beta
	sys.stdout.write('loading the model...')
	sys.stdout.flush()
	dap=bin_avg_perceptron(bias,model_path+'.model_'+str(iteration))
	# print dap.avg_weights
	sys.stdout.write('done!\n')
	sys.stdout.flush()
	dev_reader=codecs.open(dev_path,'r')
	line=dev_reader.readline()

	true_pos=0
	true_neg=0
	false_pos=0
	false_neg=0
	all_lab=0
	all_pos=0
	all_neg=0

	cnt=0
	correct=0
	while line:
		flds=line.strip().split('\t')
			
		if len(flds)>1:
			cnt+=1
			if cnt%100000==0:
				sys.stdout.write(str(cnt)+'...')
				sys.stdout.flush()
			label=flds[-1]
			feats=flds[:-1]

			prediction='1' if dap.score(feats,True)>beta else '0'
			
			all_lab+=1
			if prediction==label:
				correct+=1
				if prediction=='1':
					true_pos+=1
					all_pos+=1
				else:
					true_neg+=1
					all_neg+=1
			else:
				if prediction=='0':
					false_neg+=1
					all_pos+=1
				else:
					false_pos+=1
					all_neg+=1

		line=dev_reader.readline()
	accuracy=100.0*float(correct)/cnt
	accuracy=100.0*float(true_pos+true_neg)/all_lab
	recall=100.0*float(true_pos)/all_pos
	precision=0
	if (true_pos+false_pos)!=0:
		precision=100.0*float(true_pos)/(true_pos+false_pos)
	true_negative_rate=100.0*float(true_neg)/all_neg
	sys.stdout.write('\naccuracy of dev for iteration '+str(iteration+1)+': '+str(accuracy)+'\n')
	sys.stdout.write('recall of dev for iteration '+str(iteration+1)+': '+str(recall)+'\n')
	sys.stdout.write('precision of dev for iteration '+str(iteration+1)+': '+str(precision)+'\n')
	sys.stdout.write('true_negative_rate of dev for iteration '+str(iteration+1)+': '+str(true_negative_rate)+'\n')
	lst=[str(true_pos),str(true_neg),str(false_pos),str(false_neg),str(all_lab)]
	sys.stdout.write('tp,tn,fp,fn,all_lab: '+' '.join(lst)+'\n')
	sys.stdout.flush()


