import os,sys,codecs,operator
from collections import defaultdict

clusters = dict()
frequent_words = set()

print 'reading dics'
reader = codecs.open(os.path.abspath(sys.argv[1]),'r')
line = reader.readline()
while line:
	spl = line.strip().split(' ')
	if len(spl)==2:
		clusters[spl[0]] = 'cluster_'+spl[1]
	line = reader.readline()


print 'reading freq words'
frequent_words = set(codecs.open(os.path.abspath(sys.argv[2]),'r').read().strip().split('\n'))

reader = codecs.open(os.path.abspath(sys.argv[3]),'r')
writer = codecs.open(os.path.abspath(sys.argv[4]),'w')
line = reader.readline()

num_preserved = 0
preserved = set()
num_cluster = 0
cluster_pres = set()
num_oov = 0
oov_pres = set()
while line:
	spl = line.strip().split('\t')
	if len(spl)>2:
		if not spl[1] in frequent_words:
			if clusters.has_key(spl[1]):
				spl[1] = clusters[spl[1]]
				cluster_pres.add(spl[1])
				num_cluster+=1
			else:
				oov_pres.add(spl[1])
				spl[1] = '_unk_'
				num_oov += 1
		else:
			num_preserved+= 1
			preserved.add(spl[1])
	writer.write('\t'.join(spl)+'\n')
	line = reader.readline()
writer.close()

print 'num_preserved:', num_preserved
print 'preserved:', len(preserved)
print 'num_cluster:', num_cluster
print 'cluster_pres:', len(cluster_pres)
print 'num_oov:', num_oov
print 'oov_pres:', len(oov_pres)
