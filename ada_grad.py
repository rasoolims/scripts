import pickle,os,sys,codecs
from collections import defaultdict

class AdaGrad:
    ''' 
        this is an implementation of binary AdaGrad
    '''

    def __init__(self,model_path):
        x=self.load_model(model_path)
        self.weights=x[0]
        self.labels=x[1]

    def __init__(self,learningRate,ridge):
        self.weights=defaultdict(float)
        self.g_diag=defaultdict(float)
        self.learning_rate=learningRate
        self.ridge=ridge
        self.iteration=1
        self.labels=set()

    def update_weights(self,feature,true_label,change):
        self.g_diag[feature]=self.g_diag[feature]+math.pow(change,2)
        self.weights[feature]=self.weights[feature]+self.learning_rate*(1.0/(self.ridge+math.sqrt(self.g_diag[feature])))*change;


    def score(self,features):
        value=0.0
        for feat in features:
            value+=self.weights[feat]
        return value

    def save_model(self,model_path):
        pickle.dump([self.weights,self.labels],open(model_path,'wb'))

    def load_model(self,model_path):
        return pickle.load(open(model_path,'rb'))

    def size(self):
        return len(self.weights)
    

if __name__=='__main__':
    if len(sys.argv)<4:
        print 'python ada_grad.py [train_data] [dev_path] [model_path] [iter_num]'
        sys.exit(0)

    ada=AdaGrad(1,0.1)
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
                if cnt%100000==0:
                    sys.stdout.write(str(cnt)+'('+str(ada.size())+')'+'...')
                    sys.stdout.flush()
                label=flds[-1]
                ada.labels.add(label)
                feats=flds[:-1]

                argmax=ada.argmax(feats,False)
                if argmax!=label:
                    ada.update_weight('label:'+label,1.0)
                    ada.update_weight('label:'+argmax,-1.0)
                    for feature in feats:
                        ada.update_weight(feature+'_'+label,1.0)
                        ada.update_weight(feature+'_'+argmax,-1.0)
                else:
                    correct+=1
                ada.inc_iteration()

            line=reader.readline()
        accuracy=100.0*float(correct)/cnt
        sys.stdout.write('\naccuracy for iteration '+str(iteration+1)+': '+str(accuracy)+'\n')
        sys.stdout.write('saving the model...')
        sys.stdout.flush()
        ada.save_model(model_path+'.model_'+str(iteration+1),model_path+'.lab')
        sys.stdout.write('done!\n')
        sys.stdout.flush()
        sys.stdout.write('loading the model...')
        sys.stdout.flush()
        dada=avg_perceptron(model_path+'.model_'+str(iteration+1),model_path+'.lab')
        # print dada.avg_weights
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

                argmax=dada.argmax(feats,True) #todo
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
        sys.stdout.write('\nada iteration '+str(ada.iteration)+'\n')
        sys.stdout.write('bias/avg_bias(1) '+str(ada.weights['label:1'])+' / '+str(dada.avg_weights['label:1'])+'\n')
        sys.stdout.write('bias/avg_bias(0) '+str(ada.weights['label:0'])+' / '+str(dada.avg_weights['label:0'])+'\n')
        accuracy=100.0*float(true_pos+true_neg)/all_lab
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
    sys.stdout.write('\n'+str(ada.size())+'\n')
    sys.stdout.flush()


