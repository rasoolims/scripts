import os,sys,codecs
from collections import defaultdict

input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'


en_web_text = open(input_folder+'English-WEB_English/English-WEB.txt','r').read().strip().split('\n')
en_text = open(input_folder+'English-WEB_English/English.txt','r').read().strip().split('\n')

en2wb = {}
assert len(en_web_text)==len(en_text)
for i in xrange(len(en_text)):
	en2wb[en_text[i].strip()] = en_web_text[i].strip()

i = 0
for flat_dir in os.listdir(input_folder):
	if flat_dir == 'English-WEB_English': continue
	print flat_dir
	l_name = flat_dir[:flat_dir.find('_')]
	en_text = open(input_folder+flat_dir+'/English.txt','r').read().strip().split('\n')
	f_text = open(input_folder+flat_dir+'/'+l_name+'.txt','r').read().strip().split('\n')

	assert len(f_text)==len(en_text)
	writer_e = codecs.open(output_folder+'/'+'English'+'2'+l_name.replace('-NT',''),'w')
	writer_f = codecs.open(output_folder+'/'+l_name.replace('-NT','')+'2'+'English','w')
	for i in xrange(len(en_text)):
		writer_e.write(en_text[i].strip()+'\n')
		writer_f.write(f_text[i].strip()+'\n')

		if en_text[i].strip() in en2wb:
			writer_e.write(en2wb[en_text[i].strip()]+'\n')
			writer_f.write(f_text[i].strip()+'\n')
	writer_f.close()
	writer_e.close()
