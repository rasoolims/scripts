import os,sys,codecs,random
from collections import defaultdict

target_lang = sys.argv[3] 
dic_reader = codecs.open(os.path.abspath(sys.argv[1]),'r')
trans = dict()
for line in dic_reader:
	spl = line.strip().split('\t')
	word,lang = spl[0],spl[1]
	if lang == target_lang:
		t = set()
		for i in range(2,len(spl)):
			t.add(spl[i].replace('_',' '))
		trans[word] = t
writer =codecs.open(os.path.abspath(sys.argv[4]),'w')

percent,all_t  =0,0
for line in codecs.open(os.path.abspath(sys.argv[2]),'r'):
	try:
		sen,label = line.strip().split('\t')
		output = []
		for word in sen.strip().split():
			if word in trans: 
				percent+=1
				output.append(random.sample(trans[word],1)[0])
			else:
				output.append(word)
			all_t += 1
		if len(output)>0: writer.write(' '.join(output)+'\t'+label+'\n')
	except: print line
writer.close()
print float(percent)/all_t