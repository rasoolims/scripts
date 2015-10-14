from collections import defaultdict
import pickle,os,sys,codecs

class avg_perceptron:
	def __init__(self,model_path='',label_path=''):
		self.avg_weights=self.load_model(model_path)
		self.labels=self.load_labels(label_path)
		self.weights=defaultdict(int)
		self.iteration=1

	def update_weight(self,feature,update):
		self.weights[feature]+=update
		self.avg_weights[feature]+=iteration*update

	def score(self,features,label,is_decode):
		score=0
		if is_decode:
			score+=self.avg_weights['label:'+label]
			for feature in features:
				score+=self.avg_weights[feature+'_'+label]
		else:
			score+=self.weights['label:'+label]
			for feature in features:
				score+=self.weights[feature+'_'+label]
		return score

	def inc_iteration(self):
		self.iteration+=1

	def save_model(self,model_path,lab_path):
		avg=defaultdict(float)
		for feature in self.weights.keys():
			avg[feature]=float(self.weights[feature])-float(self.avg_weights[feature])/self.iteration
		pickle.dump(avg,open(model_path,'wb'))
		pickle.dump(self.labels,open(lab_path,'wb'))

	def load_model(self,model_path):
		if model_path!='':
			return pickle.load(open(model_path,'rb'))
		else:
			return defaultdict(float)

	def load_labels(self,model_path):
		if model_path!='':
			return pickle.load(open(model_path,'rb'))
		else:
			return set() 

	def argmax(self,features,is_decode):
		am=''
		ms=-float('inf')
		for label in self.labels:
			score=self.score(features,label,is_decode)
			#if is_decode:
				#print label,score,is_decode
			if score>ms:
				ms=score
				am=label
		#if is_decode:
			#print 'argmax:',am,ms
		return am

	def size(self):
		return len(self.avg_weights)

if __name__=='__main__':
	if len(sys.argv)<4:
		print 'python avg_perceptron.py [train_data] [dev_path] [model_path] [iter_num]'
		sys.exit(0)

	ap=avg_perceptron()
	dev_path=os.path.abspath(sys.argv[2])
	model_path=os.path.abspath(sys.argv[3])
	iter_num=int(sys.argv[4])
	
	for iteration in range(0,iter_num):
		reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
		line=reader.readline()
		cnt=0
		correct=0
		while line:
			flds=line.strip().split('\t')
			
			if len(flds)>1:
				cnt+=1
				if cnt%1000==0:
					sys.stdout.write(str(cnt)+'('+str(ap.size())+')'+'...')
					sys.stdout.flush()
				label=flds[-1]
				ap.labels.add(label)
				feats=flds[:-1]

				argmax=ap.argmax(feats,False)
				if argmax!=label:
					ap.update_weight('label:'+label,1.0)
					ap.update_weight('label:'+argmax,-1.0)
					for feature in feats:
						ap.update_weight(feature+'_'+label,1.0)
						ap.update_weight(feature+'_'+argmax,-1.0)
				else:
					correct+=1
				ap.inc_iteration()

			line=reader.readline()
		accuracy=100.0*float(correct)/cnt
		sys.stdout.write('\naccuracy for iteration '+str(iteration+1)+': '+str(accuracy)+'\n')
		sys.stdout.write('saving the model...')
		sys.stdout.flush()
		ap.save_model(model_path+'.model_'+str(iteration+1),model_path+'.lab')
		sys.stdout.write('done!\n')
		sys.stdout.flush()
		sys.stdout.write('loading the model...')
		sys.stdout.flush()
		dap=avg_perceptron(model_path+'.model_'+str(iteration+1),model_path+'.lab')
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
				if cnt%1000==0:
					sys.stdout.write(str(cnt)+'...')
					sys.stdout.flush()
				label=flds[-1]
				feats=flds[:-1]

				argmax=dap.argmax(feats,True) #todo
				all_lab+=1
				if argmax==label:
					#print 'correct',argmax,label
					correct+=1
					if argmax=='1':
						true_pos+=1
						all_pos+=1
					else:
						true_neg+=1
						all_neg+=1
				else:
					#print 'incorrect',argmax,label
					if argmax=='0':
						false_neg+=1
						all_pos+=1
					else:
						false_pos+=1
						all_neg+=1


			line=dev_reader.readline()
		accuracy=100.0*float(correct)/cnt
		sys.stdout.write('\naccuracy of dev for iteration '+str(iteration+1)+': '+str(accuracy)+'\n')
		sys.stdout.write('\nap iteration '+str(ap.iteration)+'\n')
		sys.stdout.write('bias/avg_bias(1) '+str(ap.weights['label:1'])+' / '+str(dap.avg_weights['label:1'])+'\n')
		sys.stdout.write('bias/avg_bias(0) '+str(ap.weights['label:0'])+' / '+str(dap.avg_weights['label:0'])+'\n')
		accuracy=100.0*float(true_pos+true_neg)/all_lab
		if all_pos==0:
			all_pos = 1
		recall=100.0*float(true_pos)/all_pos
		precision=0.0
		true_negative_rate=0.0
		if true_pos+false_pos>0:
			precision=100.0*float(true_pos)/(true_pos+false_pos)
		if true_neg+false_neg>0:
			true_negative_rate=100.0*float(true_neg)/(true_neg+false_neg)
		sys.stdout.write('\naccuracy of dev for iteration '+str(iteration+1)+': '+str(accuracy)+'\n')
		sys.stdout.write('recall of dev for iteration '+str(iteration+1)+': '+str(recall)+'\n')
		sys.stdout.write('precision of dev for iteration '+str(iteration+1)+': '+str(precision)+'\n')
		sys.stdout.write('true_negative_rate of dev for iteration '+str(iteration+1)+': '+str(true_negative_rate)+'\n')
		lst=[str(true_pos),str(true_neg),str(false_pos),str(false_neg),str(all_lab)]
		sys.stdout.write('tp,tn,fp,fn,all_lab: '+' '.join(lst)+'\n')
	sys.stdout.write('\n'+str(ap.size())+'\n')
	sys.stdout.flush()


