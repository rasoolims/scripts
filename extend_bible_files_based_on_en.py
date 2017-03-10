import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<2:
	print 'input_folder'

input_folder = os.path.abspath(sys.argv[1])+'/'

en2target = defaultdict(dict)

langs = set()
i = 0
print 'creating dictionaries'
for f in os.listdir(input_folder):
	l1,l2 = f.split('2')
	if l1 == 'en':
		print l2
		f1 = input_folder + l1+'2'+l2
		f2 = input_folder + l2+'2'+l1
		langs.add(l2)

		en_text = codecs.open(f1,'r').read().strip().split('\n')
		f_text = codecs.open(f2,'r').read().strip().split('\n')

		assert len(en_text) == len(f_text)

		for i in xrange(len(en_text)):
			en2target[en_text[i]][l2] = f_text[i]


print 'extending'
for l1 in langs:
	for l2 in langs:
		if l1 >= l2: continue
		print l1,l2
		writer1 = codecs.open(input_folder+l1+'2'+l2,'w')
		writer2 = codecs.open(input_folder+l2+'2'+l1,'w')

		for en_text in en2target.keys():
			if l1 in en2target[en_text] and l2 in en2target[en_text]:
				writer1.write(en2target[en_text][l1]+'\n')
				writer2.write(en2target[en_text][l2]+'\n')
		writer1.close()
		writer2.close()
