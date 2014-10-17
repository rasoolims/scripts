import sys,os,codecs,pickle
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
model_path=os.path.abspath(sys.argv[2])

features=list()
labels=list()

# reading data into features and labels
print 'reading data into features and labels'
sys.stdout.flush()

line=reader.readline()
while line:
	line=line.strip()
	if line:
		spl=line.split('\t')
		feat_dict=dict()
		for i in range(0,len(spl)-1):
			feat_dict[spl[i]]=1
		features.append(feat_dict)
		labels.append(int(spl[len(spl)-1]))
	line=reader.readline()

print 'loading to the model files'
sys.stdout.flush()

classifier= pickle.load(open(model_path+'.model','rb'))
vectorizer=pickle.load(open(model_path+'.bin','rb'))

print 'binarizing features'
sys.stdout.flush()

bin_feats=vectorizer.transform(features)


print 'predicting values'
sys.stdout.flush()

cor=0
prediction=classifier.predict(bin_feats)

false_positive=0
true_positive=0
true_negative=0
false_negative=0
for i in range(0,len(prediction)):
	if labels[i]==prediction[i]:
		cor+=1
		if labels[i]==1:
			true_positive+=1
		else:
			true_negative+=1
	elif labels[i]==1:
		false_positive+=1
	else:
		false_negative+=1

print cor,len(prediction)
print true_positive,true_negative,false_positive,false_negative
