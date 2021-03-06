# coding: utf8
import os,sys,codecs


sens=codecs.open(os.path.abspath(sys.argv[1]),'r',encoding='utf8').read().strip().split('\n')

spacing=False
if len(sys.argv)>3 and sys.argv[3]=='true':
	spacing=True
output=list()

for sen in sens:
	pr=sen
	if spacing:
		pr=sen.replace('  ','\t').replace(' ','').replace('\t',' ').strip()
	ws=pr.split(' ')
	o=list()
	for w in ws:
		if w.endswith(','):
			w=w[:-1]+' '+','
		if w.endswith(u'、'):
			w=w[:-1]+u' 、'
		o.append(w)
	output.append((' '.join(o)).replace('  ',' ').replace('  ',' ').replace('  ',' '))

codecs.open(os.path.abspath(sys.argv[2]),'w',encoding='utf8').write('\n'.join(output))

print 'done!'