import os,sys,codecs

'''
	cats all files together
'''

path=os.path.abspath(sys.argv[1])
writer=codecs.open(os.path.abspath(sys.argv[2]),'w')
extension=sys.argv[3]

for root, dirs, files in os.walk(path):
	for name in files:
		if name.endswith(extension):
			full_path=root+'/'+name
			
			content=codecs.open(full_path,'r').read()
			writer.write(content)

			print full_path
writer.flush()
writer.close()
print 'done!'