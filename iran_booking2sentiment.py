from __future__ import unicode_literals
import urllib2,os,codecs,sys
from lxml import html
from hazm import *

normalizer = Normalizer()

all_comments = []
stars = []
sentiments = []
writer1 = codecs.open(os.path.abspath(sys.argv[1]),'w',encoding='utf-8')
writer2 = codecs.open(os.path.abspath(sys.argv[2]),'w',encoding='utf-8')
for i in range(1,77):
	url = 'http://www.iran-booking.com/reviews/page/'+str(i)
	print url

	response = urllib2.urlopen(url)
	webContent = unicode(response.read(),'utf-8').replace('<br />','')

	#parser = BookingHTMLParser()
	#parser.feed(webContent)


	tree = html.fromstring(webContent)
	comments = tree.xpath('//div[@class="body"]/text()')
	imgs = tree.xpath("//div[@class='body']/p/img/@src")

	assert len(comments) == len(imgs)
	for img in imgs:
		star = img.replace('http://www.iran-booking.com/images/','').replace('stars.png','')
		stars.append(star)

		if int(star)<=2:
			sentiments.append('negative')
		elif int(star)==3:
			sentiments.append('neutral')
		else:
			sentiments.append('positive')
	for comment in comments:
		try:
			comment = ' '.join(word_tokenize(normalizer.normalize(comment))).replace('_',' ').replace('  ',' ')
		except:
			print comment
			comment = ''

		all_comments.append(comment)

for i in xrange(len(all_comments)):
	if len(all_comments[i])>0:
		writer1.write(all_comments[i]+'\t'+stars[i]+'\n')
		writer2.write(all_comments[i]+'\t'+sentiments[i]+'\n')
writer1.close()
writer2.close()
