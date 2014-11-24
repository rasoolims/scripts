from collections import defaultdict
import pickle,os,sys,codecs

class bin_avg_perceptron:
	def __init__(self,bias,model_path=''):
		self.avg_weights=self.load_model(model_path)
		self.weights=defaultdict(int)
		self.iteration=1
		self.bias=bias
		self.avg_bias=bias
		if model_path!='':
			self.avg_bias=float(pickle.load(open(model_path+'.bias','rb')))

	def update_weight(self,feature,update):
		self.weights[feature]+=update
		self.avg_weights[feature]+=iteration*update

	def score(self,features,is_decode):
		score=0
		if is_decode:
			score+=self.avg_bias
			for feature in features:
				score+=self.avg_weights[feature]
		else:
			score+=self.bias
			for feature in features:
				score+=self.weights[feature]
		return score

	def label(self,features,is_decode,beta):
		if self.score(features,is_decode)>beta:
			return '1'
		return '0'

	def inc_iteration(self):
		self.iteration+=1

	def save_model(self,model_path):
		avg=defaultdict(float)
		for feature in self.weights.keys():
			avg[feature]=float(self.weights[feature])-float(self.avg_weights[feature])/self.iteration
		pickle.dump(avg,open(model_path,'wb'))
		pickle.dump(float(self.avg_bias)/self.iteration,open(model_path+'.bias','wb'))


	def load_model(self,model_path):
		if model_path!='':
			return pickle.load(open(model_path,'rb'))
		else:
			return defaultdict(float)

	def size(self):
		return len(self.avg_weights)

if __name__=='__main__':
	if len(sys.argv)<4:
		print 'python bin_avg_perceptron.py [train_data] [dev_path] [model_path] [iter_num] [threshold(optional; default:0)] [bias(optional;default:0)]'
		sys.exit(0)

	beta=0
	bias=0
	if len(sys.argv)>5:
		beta=float(sys.argv[5])
	if len(sys.argv)>6:
		bias=float(sys.argv[6])
	ap=bin_avg_perceptron(bias)
	dev_path=os.path.abspath(sys.argv[2])
	model_path=os.path.abspath(sys.argv[3])
	iter_num=int(sys.argv[4])
	
	print 'threshold',beta
	print 'bias',bias
	for iteration in range(0,iter_num):
		reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
		line=reader.readline()
		cnt=0
		correct=0
		while line:
			flds=line.strip().split('\t')
			
			if len(flds)>1:
				cnt+=1
				if cnt%100000==0:
					sys.stdout.write(str(cnt)+'('+str(ap.size())+')'+'...')
					sys.stdout.flush()
				label=flds[-1]
				feats=flds[:-1]

				prediction='1' if ap.score(feats,False)>beta else '0'
				if prediction!=label:
					if prediction=='1':
						ap.avg_bias+=ap.iteration*-1.0
						ap.bias+=-1.0
					else:
						ap.bias+=1.0
						ap.avg_bias+=ap.iteration*1.0

					for feature in feats:
						if prediction=='1':
							ap.update_weight(feature,-1.0)
						else:
							ap.update_weight(feature,1.0)
				else:
					correct+=1
				ap.inc_iteration()

			line=reader.readline()
		accuracy=100.0*float(correct)/cnt
		sys.stdout.write('\naccuracy for iteration '+str(iteration+1)+': '+str(accuracy)+'\n')
		sys.stdout.write('current bias: '+str(ap.bias)+'\n')
		sys.stdout.write('saving the model...')
		sys.stdout.flush()
		ap.save_model(model_path+'.model_'+str(iteration+1))
		sys.stdout.write('done!\n')
		sys.stdout.flush()
		sys.stdout.write('loading the model...')
		sys.stdout.flush()
		dap=bin_avg_perceptron(bias,model_path+'.model_'+str(iteration+1))
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
		sys.stdout.write('\naccuracy of dev for iteration '+str(iteration+1)+': '+str(accuracy)+'\n')

		accuracy=100.0*float(true_pos+true_neg)/all_lab
		recall=100.0*float(true_pos)/all_pos
		precision=0

		if (true_pos+false_pos)!=0:
			precision=100.0*float(true_pos)/(true_pos+false_pos)
		true_negative_rate=100.0*float(true_neg)/(true_neg+false_neg)
		sys.stdout.write('\naccuracy of dev for iteration '+str(iteration+1)+': '+str(accuracy)+'\n')
		sys.stdout.write('recall of dev for iteration '+str(iteration+1)+': '+str(recall)+'\n')
		sys.stdout.write('precision of dev for iteration '+str(iteration+1)+': '+str(precision)+'\n')
		sys.stdout.write('true_negative_rate of dev for iteration '+str(iteration+1)+': '+str(true_negative_rate)+'\n')
		lst=[str(true_pos),str(true_neg),str(false_pos),str(false_neg),str(all_lab)]
		sys.stdout.write('tp,tn,fp,fn,all_lab: '+' '.join(lst)+'\n')
	sys.stdout.write('\n'+str(ap.size())+'\n')
	sys.stdout.flush()


