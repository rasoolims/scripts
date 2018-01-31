from __future__ import unicode_literals
import os,sys,codecs
from collections import defaultdict
reload(sys)
sys.setdefaultencoding('utf8')

if len(sys.argv)<3:
	print 'input_folder  untok_uniq_folder  tok_uniq_folder output_folder'
	sys.exit(0)
input_folder = os.path.abspath(sys.argv[1])+'/'
untok_uniq_folder = os.path.abspath(sys.argv[2])+'/'
tok_uniq_folder = os.path.abspath(sys.argv[3])+'/'
output_folder = os.path.abspath(sys.argv[4])+'/'

tok_dict = dict()

for f in os.listdir(untok_uniq_folder):
	tok_dict[f] = dict()
	untok = codecs.open(untok_uniq_folder+f,'r',encoding='utf-8').read().strip().split('\n')
	tok = codecs.open(tok_uniq_folder+f,'r',encoding='utf-8').read().strip().split('\n')
	assert len(tok)==len(untok)
	for i in xrange(len(tok)):
		tok_dict[f][untok[i].strip()] = tok[i].strip()


commands = list()
for f in os.listdir(input_folder):
	dest = f.split('.')[1]
	print f

	writer = codecs.open(output_folder+f,'w',encoding='utf-8')
	lines = codecs.open(input_folder+f,'r',encoding='utf-8').read().strip().split('\n')
	for l in lines:
		output = []
		if len(l.strip())>0:
			#if dest=='zh':
			#	writer.write(l.strip()+'\n')
			#else:
			writer.write(tok_dict[dest][l.strip()]+'\n')	
		else:
			writer.write(l.strip()+'\n')
	writer.close()
print 'done!'