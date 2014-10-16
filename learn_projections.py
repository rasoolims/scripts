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

# creating feature binarizer
vectorizer = DictVectorizer(sparse=True)
print 'binarizing features'
sys.stdout.flush()
bin_feats=vectorizer.fit_transform(features)

classifier = svm.SVC()#kernel='poly',degree=2,coef0=1
print 'learning model'
sys.stdout.flush()
classifier.fit(bin_feats,labels)

print 'serializing to the file'
sys.stdout.flush()
pickle.dump(classifier,open(model_path+'.model','wb'))
pickle.dump(vectorizer,open(model_path+'.bin','wb'))

print 'done!'
sys.stdout.flush()
