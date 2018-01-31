import re,os,sys,codecs,traceback
from xml.dom import minidom

'''
	The input folder is the folder with Bible xml files from https://github.com/christos-c/bible-corpus/
	The output folder contains aligned files for all pairs of languages (src.target)
	It merges English and English-Web files.
'''
if len(sys.argv)<3:
	print 'input_folder output_folder'
	sys.exit(0)

inp_folder = os.path.abspath(sys.argv[1])+'/'
output_folder = os.path.abspath(sys.argv[2])+'/'
bible_dict = dict()
langs = set()
for f in os.listdir(inp_folder):
	if f!='cop.xml' and f != 'en_web.xml' and len(f)>6: continue
	print f
	try:
		xmldoc = minidom.parse(inp_folder+f)
		sentences = xmldoc.getElementsByTagName('seg')
		bible_dict[f] = dict()
		for sentence in sentences:
			sen_id = sentence.attributes['id'].value
			try:
				s =  sentence.firstChild.nodeValue.replace('\n',' ').replace('\t',' ').strip()
				end_id = sen_id[sen_id.rfind('.')+1:]
				if s != end_id:
					bible_dict[f][sen_id] = s
			except: pass
		print len(bible_dict[f])
	except:
		print f
		traceback.print_exc(file=sys.stdout)

print 'saving bibles'
for f1 in bible_dict.keys():
	if f1 == 'en_web.xml': continue
	for f2 in bible_dict.keys():
		if f1>=f2 or f2 == 'en_web.xml': continue

		l1 = f1[:f1.find('.')]
		l2 = f2[:f2.find('.')]
		print l1,l2
		w1 = codecs.open(output_folder+l2+'.'+l1,'w',encoding='utf-8')
		w2 = codecs.open(output_folder+l1+'.'+l2,'w',encoding='utf-8')

		shared_sentences = set(bible_dict[f1].keys()) & set(bible_dict[f2].keys())
		for s in shared_sentences:
			w1.write(bible_dict[f1][s]+'\n')
			w2.write(bible_dict[f2][s]+'\n')

		# Merging with English-Web
		if l1 == 'en':
			shared_sentences = set(bible_dict['en_web.xml'].keys()) & set(bible_dict[f2].keys())
			for s in shared_sentences:
				w1.write(bible_dict['en_web.xml'][s]+'\n')
				w2.write(bible_dict[f2][s]+'\n')

		if l2 == 'en':
			shared_sentences = set(bible_dict[f1].keys()) & set(bible_dict['en_web.xml'].keys())
			for s in shared_sentences:
				w1.write(bible_dict[f1][s]+'\n')
				w2.write(bible_dict['en_web.xml'][s]+'\n')

		w1.close()
		w2.close()
print 'done!'