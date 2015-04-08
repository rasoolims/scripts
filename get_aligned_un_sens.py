import os,sys,codecs
from collections import defaultdict

path=os.path.abspath(sys.argv[1])
outputdir=os.path.abspath(sys.argv[2])+'/'
extension='.snt'
langs=set(['en','fr','de','ru','ar','zh','es'])


lang_file_list=defaultdict(dict)

for root, dirs, files in os.walk(path):
	for name in files:
		if name.endswith(extension):
			full_path=root+'/'+name
			
			langId=name[name.rfind('_')+1:name.rfind('.snt')]
			pattern=name[:name.rfind('_')]
			lang_file_list[langId][pattern]=full_path

			#print full_path

writers=defaultdict()
for l1 in lang_file_list.keys():
	for l2 in lang_file_list.keys():
		if l2==l1:
			continue
		writers[l1+'_'+l2]=codecs.open(outputdir+l1+'_'+l2,'w')

for l1 in lang_file_list.keys():
	print 'l1 '+l1
	for l2 in lang_file_list.keys():
		if l1==l2:
			continue
		print 'l1,l2',l1,l2
		for pattern in lang_file_list[l1].keys():
			if  lang_file_list[l2].has_key(pattern):
				writers[l1+'_'+l2].write(codecs.open(lang_file_list[l1][pattern],'r').read()+'\n')

for l1 in lang_file_list.keys():
	for l2 in lang_file_list.keys():
		if l1==l2:
			continue
		writers[l1+'_'+l2].flush()
		writers[l1+'_'+l2].close()
print 'done!'