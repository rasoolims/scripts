import sys,codecs,os

predicted_reader=codecs.open(os.path.abspath(sys.argv[1]),'r')
gold_reader=codecs.open(os.path.abspath(sys.argv[2]),'r')

line=predicted_reader.readline()
corr=0
all_t=0
all_sen=0
corr_sen=0

while line:
	spl=line.strip().split(' ')
	gline=gold_reader.readline()
	gspl=gline.strip().split(' ')
	if len(spl)!=len(gspl):
		print spl
		print gspl
	output=list()
	all_c=True
	for i in range(0,len(spl)):
		tag1=spl[i][spl[i].rfind('_')+1:]
		tag2=gspl[i][gspl[i].rfind('_')+1:]

		if tag2==tag1:
			corr+=1
		else:
			all_c=False
		all_t+=1
	if all_c:
		corr_sen+=1
	all_sen+=1
	
	line=predicted_reader.readline()

acc=float(corr)*100.0/all_t
exact=float(corr_sen)*100.0/all_sen

print acc,exact
