import os,sys,codecs
from os import listdir
from os.path import isfile, join

dir1=os.path.abspath(sys.argv[1])

l1=sys.argv[2]
l2=sys.argv[3]

writer1=codecs.open(os.path.abspath(sys.argv[4])+'.'+l1,'w')
writer2=codecs.open(os.path.abspath(sys.argv[4])+'.'+l2,'w')


for d in os.listdir(dir1):
	#print dir1
	#print d
	dir2=dir1+'/'+d
	fs= listdir(dir2)

	if l1+'.txt' in fs and l2+'.txt' in fs:
		c1=codecs.open(dir2+'/'+l1+'.txt','r').read()
		c2=codecs.open(dir2+'/'+l2+'.txt','r').read()

		output=list()
		for c in c1.split('\n'):
			if c.strip():
				output.append(c.strip())
		c1='\n'.join(output)

		output=list()
		for c in c2.split('\n'):
			if c.strip():
				output.append(c.strip())
		c2='\n'.join(output)


		if len(c1.split('\n'))>len(c2.split('\n')):
			print dir2
			print len(c1.split('\n')),len(c2.split('\n'))
		else:
			writer1.write(c1)
			writer2.write(c2)

writer1.close()
writer2.close()

