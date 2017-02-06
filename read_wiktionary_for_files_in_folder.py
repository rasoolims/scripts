import urllib2,json,os,sys,codecs
from collections import defaultdict


input_folder = os.path.abspath(sys.argv[1])+'/'
writer = codecs.open(os.path.abspath(sys.argv[2]),'w')

for f in os.listdir(input_folder):
	words = codecs.open(input_folder+f,'r').read().strip().split('\n')
	print f
	src_lang = f
	word_dict = defaultdict()
	count = 0
	no_trans =0 
	for word in words:
		word_dict[word] = defaultdict(set)
		content =  json.loads(urllib2.urlopen("https://"+src_lang+".wiktionary.org/w/api.php?action=query&prop=iwlinks&format=json&titles="+word+"&iwlimit=500").read())
		for c in content['query']['pages']:
			try:
				for ws in content['query']['pages'][c]['iwlinks']:
					lang,translation = ws['prefix'].encode('utf-8'),ws['*'].encode('utf-8')
					translation=translation.replace('Special:Search/','').replace('_','').strip()
					if len(translation)>0: word_dict[word][lang].add()
			except: 
				#print sys.exc_info()[0]
				#print content
				no_trans+=1
		count+=1
		if count%100==0: sys.stdout.write(str(count)+'/'+str(no_trans)+'...')
	
	print '\nwriting...'
	for word in word_dict.keys():
		for lang in word_dict[word].keys():
			translations = word_dict[word][lang]
			if len(translations)>0:
				writer.write(word+'\t'+src_lang+'\t'+lang+'\t'+'\t'.join(translations)+'\n')
	writer.flush()
	
writer.close()
print 'done!'