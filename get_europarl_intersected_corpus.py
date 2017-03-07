import os,sys,codecs
from collections import defaultdict

if len(sys.argv)<3:
	print 'input_folder output_folder'
	sys.exit(0)
input_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'

en2all_dict = defaultdict(dict)

en2others_sentences = defaultdict(list)
others2en_sentences = defaultdict(list)
for f in os.listdir(input_folder):
	lang_id = f[f.rfind('.')+1:]
	other_lang = 'en'
	if lang_id == 'en':
		other_lang = f[f.find('.')+1:f.rfind('-')]
	print f,lang_id,other_lang
	lines = codecs.open(input_folder+f,'r').read().strip().split('\n')

	if other_lang=='en':
		others2en_sentences[lang_id] = lines
	else:
		en2others_sentences[other_lang] = lines

print 'creating dicts'
num_langs = len(en2others_sentences)
for lang in en2others_sentences.keys():
	print lang
	en_lines = en2others_sentences[lang]
	other_lines = others2en_sentences[lang]

	assert len(en_lines)==len(other_lines)

	for i in xrange(len(en_lines)):
		if len(en_lines[i].strip())>0 and len(other_lines[i].strip()):
			en2all_dict[en_lines[i].strip()][lang] = other_lines[i].strip()

print len(en2all_dict)

print 'pruning dicts'
for sen in en2all_dict.keys():
	if len(en2all_dict[sen])<num_langs:
		del en2all_dict[sen]

writers = {lang:codecs.open(output_folder+lang,'w') for lang in en2others_sentences.keys()}
writers['en'] = codecs.open(output_folder+'en','w')

print len(en2all_dict)

print 'final writing'
for sen in en2all_dict.keys():
	if len(sen.strip())>0:
		writers['en'].write(sen+'\n')
		for l in en2all_dict[sen].keys():
			writers[l].write(en2all_dict[sen][l]+'\n')

for l in writers.keys():
	writers[l].close()
print 'done!'