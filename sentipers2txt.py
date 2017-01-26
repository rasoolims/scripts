import re,os,sys,codecs
from xml.dom import minidom
from collections import defaultdict

writer = codecs.open(os.path.abspath(sys.argv[2]),'w',encoding = 'utf-8')

inp_folder = os.path.abspath(sys.argv[1])+'/'
v = 0
nv = 0
sentiment_dict = defaultdict(int)
for f in os.listdir(inp_folder):
	print f
	if not f.endswith('xml'): 
		if f =='Extra':
			for f2 in os.listdir(inp_folder+f):
				if f2.endswith('xml'):
					print f+'/'+f2
					sens = codecs.open(inp_folder+f+'/'+f2,'r',encoding = 'utf-8').read().strip().split('[@@@]')
					for sen in sens:
						lns = sen.strip().replace('\t',' ').split('\n')
						if len(lns)<2: continue
						try:
							sent = int(lns[-1][1:-1])
						except:
							nv+=1
							continue
						sentiment = 'positive' if sent>0 else 'negative' if sent<0 else 'neutral'
						words = []
						for i in xrange(len(lns)-1):
							if len(lns[i].strip().split())>1:
								words.append(lns[i].strip().split()[1].strip())
						
						if len(words)>0:
							v+=1
							writer.write(' '.join(words)+'\t'+sentiment+'\n')
							sentiment_dict[sentiment]+=1


	else:
		xmldoc = minidom.parse(inp_folder+f)
		sentences = xmldoc.getElementsByTagName('Sentence')
		for sentence in sentences:
			try:
				sent = int(sentence.attributes['Value'].value)
				sentiment = 'positive' if sent>0 else 'negative' if sent<0 else 'neutral'
				writer.write(sentence.firstChild.nodeValue.replace('\n',' ').replace('\t',' ').strip()+'\t'+sentiment+'\n')
				sentiment_dict[sentiment]+=1
				v+=1
			except:
				nv+=1
writer.close()

print v, nv
print sentiment_dict