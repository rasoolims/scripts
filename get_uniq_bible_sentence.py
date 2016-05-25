import os,sys,codecs
from collections import defaultdict

input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'


lang_sens = defaultdict(set)
tok_dict = defaultdict(dict)

counter = 0
print 'reading to set...'
for f in os.listdir(input_folder):
	l = f[f.rfind('.')+1:]
	counter+=1
	if counter%100==0:
		print counter
	lang_sens[l]|=set(codecs.open(input_folder+f,'r').read().strip().split('\n'))

print 'writing and tokenizing set...'
for l in lang_sens.keys():
	print l
	codecs.open(output_folder+l,'w').write('\n'.join(lang_sens[l]))
print 'done!'