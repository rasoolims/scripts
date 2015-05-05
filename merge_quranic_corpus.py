import os,sys,codecs
from os import listdir
from os.path import isfile, join

dir1=os.path.abspath(sys.argv[1])
dir2=os.path.abspath(sys.argv[2])

l1=sys.argv[4]
l2=sys.argv[5]
writer1=codecs.open(os.path.abspath(sys.argv[3])+'.'+l1,'w')
writer2=codecs.open(os.path.abspath(sys.argv[3])+'.'+l2,'w')

src_files=os.listdir(dir1)
dst_files=os.listdir(dir2)


for s in src_files:
	if not s.endswith('.txt'):
		continue
	for d in dst_files:
		if not d.endswith('.txt'):
			continue
		print s,d	

		writer1.write(codecs.open(dir1+'/'+s,'r').read())
		writer2.write(codecs.open(dir2+'/'+d,'r').read())


writer1.flush()
writer2.flush()
writer1.close()
writer2.close()