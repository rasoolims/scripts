import os,sys,codecs,random
from collections import defaultdict

print '[dic_path] [tagged_path] [out_path] [chance]'

dict_fp = codecs.open(os.path.abspath(sys.argv[1]), 'r')
src2dst_dict = dict()
for line in dict_fp:
	w,t,f = line.split()
	if not w in src2dst_dict:
		src2dst_dict[w] = list()
	for i in xrange(int(f)):
		src2dst_dict[w].append(t)
print 'loaded dictionaries'


r1 = codecs.open(os.path.abspath(sys.argv[2]),'r')
w = codecs.open(os.path.abspath(sys.argv[3]),'w')
chance = float(sys.argv[4])

counter = 0
wrote = 0
l1 = r1.readline().strip()
while l1:
	counter+=1
	if counter%100000==0:
		sys.stdout.write(str(counter)+'/'+str(wrote)+'...')
	if random.random()>chance:
		l1 = r1.readline().strip()
		continue

	src_words = []
	src_tags = []
	
	for wt in l1.split():
		i = wt.rfind('_')
		src_words.append(wt[:i].lower())
		src_tags.append(wt[i+1:])

	translations = ['_']*len(src_words)
	tt = random.randint(0,len(src_words)-1)

	picked = False
	for tt in xrange(len(src_words)):
		if src_words[tt] in src2dst_dict:
			translations[tt] = random.sample(src2dst_dict[src_words[tt]],1)[0]
			picked = True

	if picked: wrote+=1
	
	if picked:
		output = []
		for i in xrange(len(src_words)):
			o = src_words[i]+' '+src_tags[i]+' '+ translations[i]
			output.append(o)

		w.write('\n'.join(output)+'\n\n')

	l1 = r1.readline().strip()

sys.stdout.write(str(counter)+'/'+str(wrote)+'\n')
w.close()
