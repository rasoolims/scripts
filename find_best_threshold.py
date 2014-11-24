import os,sys,math,operator,codecs,traceback
from collections import defaultdict
from bin_avg_perceptron import bin_avg_perceptron

if __name__=='__main__':
	if len(sys.argv)<5:
		print 'python find_best_threshold.py [model_path] [iter_num] [start] [end] [step_size] [f_score_weight] [dev_path]'
		sys.exit(0)

	start=float(sys.argv[3])
	end=float(sys.argv[4])
	step_size=float(sys.argv[5])

	bias=0
	model_path=os.path.abspath(sys.argv[1])
	iteration=int(sys.argv[2])
	f_score_weight=float(sys.argv[6])
	dev_path=os.path.abspath(sys.argv[7])

	true_pos=dict()
	true_neg=dict()
	false_pos=dict()
	false_neg=dict()
	correct=dict()

	b=start
	while b<=end:
		true_pos[b]=0
		true_neg[b]=0
		false_pos[b]=0
		false_neg[b]=0
		correct[b]=0
		b+=step_size


	sys.stdout.write('loading the model...')
	sys.stdout.flush()
	dap=bin_avg_perceptron(bias,model_path+'.model_'+str(iteration))
	# print dap.avg_weights
	sys.stdout.write('done!\n')
	sys.stdout.flush()
	dev_reader=codecs.open(dev_path,'r')
	line=dev_reader.readline()

	all_lab=0
	all_pos=0
	all_neg=0

	cnt=0
	while line:
		flds=line.strip().split('\t')
			
		if len(flds)>1:
			cnt+=1
			if cnt%100000==0:
				sys.stdout.write(str(cnt)+'...')
				sys.stdout.flush()
			label=flds[-1]
			feats=flds[:-1]

			all_lab+=1

			if label=='1':
				all_pos+=1
			else:
				all_neg+=1
			
			beta=start
			while beta<=end:
				prediction='1' if dap.score(feats,True)>beta else '0'
				
				if prediction==label:
					correct[beta]+=1
					if prediction=='1':
						true_pos[beta]+=1
					else:
						true_neg[beta]+=1
				else:
					if prediction=='0':
						false_neg[beta]+=1
					else:
						false_pos[beta]+=1
				beta+=step_size

		line=dev_reader.readline()
	
	beta=start
	while beta<=end:
		accuracy=100.0*float(correct[beta])/cnt
		accuracy=100.0*float(true_pos[beta]+true_neg[beta])/all_lab
		recall=100.0*float(true_pos[beta])/all_pos
		precision=0
		if (true_pos[beta]+false_pos[beta])!=0:
			precision=100.0*float(true_pos[beta])/(true_pos[beta]+false_pos[beta])
		true_negative_rate=100.0*float(true_neg[beta])/(true_neg[beta]+false_neg[beta])
		sys.stdout.write('\naccuracy of dev for beta '+str(beta)+': '+str(accuracy)+'\n')
		sys.stdout.write('recall of dev for beta '+str(beta)+': '+str(recall)+'\n')
		sys.stdout.write('precision of dev for beta '+str(beta)+': '+str(precision)+'\n')
		sys.stdout.write('true_negative_rate of dev for beta '+str(beta)+': '+str(true_negative_rate)+'\n')
		lst=[str(true_pos[beta]),str(true_neg[beta]),str(false_pos[beta]),str(false_neg[beta]),str(all_lab)]
		sys.stdout.write('tp,tn,fp,fn,all_lab: '+' '.join(lst)+'\n')
		f_score=(1+f_score_weight)*(precision*recall)/(f_score_weight*f_score_weight*precision+recall)
		sys.stdout.write('f_b score for beta='+str(beta)+': '+str(f_score)+'\n\n')
		sys.stdout.flush()
		beta+=step_size


