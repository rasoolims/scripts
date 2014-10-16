import sys,os,codecs,pickle
from sklearn.feature_extraction import DictVectorizer
from sklearn import svm

reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
model_path=os.path.abspath(sys.argv[2])

features=list()
labels=list()

# reading data into features and labels
print 'reading data into features and labels'
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
classifier= pickle.load(open(model_path+'.model','rb'))
vectorizer=pickle.load(open(model_path+'.bin','rb'))

print 'binarizing features'
bin_feats=vectorizer.transform(features)


print 'predicting values'
cor=0
prediction=classifier.predict(bin_feats)
for i in range(0,len(prediction)):
	if labels[i]==prediction[i]:
		cor+=1

print cor,len(prediction)
