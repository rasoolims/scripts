import urllib2,json,os,sys,codecs
from collections import defaultdict

word_dict = defaultdict()
words = codecs.open(os.path.abspath(sys.argv[1]),'r').read().strip().split('\n')
src_lang = sys.argv[2]

count = 0
no_trans =0 
for word in words:
	word_dict[word] = defaultdict(set)
	content =  json.loads(urllib2.urlopen("https://"+src_lang+".wiktionary.org/w/api.php?action=query&prop=iwlinks&format=json&titles="+word+"&iwlimit=500").read())
	for c in content['query']['pages']:
		try:
			for ws in content['query']['pages'][c]['iwlinks']:
				lang,translation = ws['prefix'].encode('utf-8'),ws['*'].encode('utf-8')
				word_dict[word][lang].add(translation)
		except: no_trans+=1
	count+=1
	if count%100==0: sys.stdout.write(str(count)+'/'+str(no_trans)+'...')
writer = codecs.open(os.path.abspath(sys.argv[3]),'w')

print '\nwriting...'
for word in word_dict.keys():
	for lang in word_dict[word].keys():
		translations = word_dict[word][lang]
		writer.write(word+'\t'+lang+'\t'+'\t'.join(translations)+'\n')
writer.close()
print 'done!'