import os,sys,codecs

def is_punc(pos):
	return pos=="#" or pos=="$" or pos=="''" or pos=="(" or pos=="" or pos=="[" or pos=="]" or pos=="{" or pos=="}" or pos=="\"" or pos=="," or pos=="." or pos==":" or pos=="``" or pos=="-LRB-" or pos=="-RRB-" or pos=="-LSB-" or pos=="-RSB-" or pos=="-LCB-" or pos=="-RCB-"


all_deps=0
correct_deps=0

nall_deps=0
ncd=0

# gold
r1=codecs.open(os.path.abspath(sys.argv[1]),'r')

# predicted
r2=codecs.open(os.path.abspath(sys.argv[2]),'r')

l1=r1.readline()
while l1:
	s1=l1.strip().split('\t')
	s2=r2.readline().strip().split('\t')

	if len(s1)>6:
		try:
			if not is_punc(s1[3]):
				all_deps+=1
				if s1[6]==s2[6]:
					correct_deps+=1
			nall_deps+=1
			if s1[6]==s2[6]:
				ncd+=1
		except:
			print s2

	l1=r1.readline()

acc=100*float(correct_deps)/all_deps

print acc

acc=100*float(ncd)/nall_deps

print acc