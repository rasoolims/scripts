import os,sys,codecs
from collections import defaultdict

jar_file = os.path.abspath(sys.argv[1])
model_folder = os.path.abspath(sys.argv[2])+'/'
input_folder = os.path.abspath(sys.argv[3])+'/'
output_folder = os.path.abspath(sys.argv[4])+'/'


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
	codecs.open('/tmp/l.sens','w').write('\n'.join(lang_sens[l]))
	model = model_folder  + l
	command = 'java -jar '+ jar_file+' TokenizerME '+ model+' < '+'/tmp/l.sens'+' > '+'/tmp/l.sens.tok'
	os.system(command)
	s1 = codecs.open('/tmp/l.sens','r').read().strip().split('\n')
	t1 = codecs.open('/tmp/l.sens.tok','r').read().strip().split('\n')
	assert len(s1)==len(t1)
	for i in range(0,len(s1)):
		tok_dict[l][s1[i]] = t1[i]

command= 'rm -f /tmp/l.sens*'
os.system(command)

counter = 0
print 'tokenizing...'
for f in os.listdir(input_folder):
	l = f[f.rfind('.')+1:]
	counter+=1
	if counter%100==0:
		print counter
	sens = codecs.open(input_folder+f,'r').read().strip().split('\n')
	output = list()
	for s in sens:
		output.append(tok_dict[l][s])

	codecs.open(output_folder+f,'w').write('\n'.join(output))

print 'done!'