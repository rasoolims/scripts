# -*- coding: utf8
import os,sys,codecs

def normalize(str1):
	str1=str1.replace(u'ۀ',u'هٔ')
	return str1


c1=codecs.open(os.path.abspath(sys.argv[1]),'r',encoding='utf-8').read().strip().replace('\r','').split('\n\n')
c2=codecs.open(os.path.abspath(sys.argv[2]),'r',encoding='utf-8').read().strip().split('\n\n')
writer=codecs.open(os.path.abspath(sys.argv[3]),'w',encoding='utf-8')

sen_dic1=dict()
sen_dic2=dict()

for s in c1:
	ls=s.strip().split('\n')
	sen_num=0
	ws=list()
	for l in ls:
		if not l.strip():
			continue
		fs=l.strip().split('\t')
		if sen_num==0:
			sen_num=int(fs[5][fs[5].find('senID=')+6:])
		ws.append(normalize(fs[1]))

	sen_dic1[sen_num]=' '.join(ws)

for s in c2:
	ls=s.strip().split('\n')
	sen_num=0
	ws=list()
	for l in ls:
		if not l.strip():
			continue
		fs=l.strip().split('\t')
		if sen_num==0:
			sen_num=int(fs[5][fs[5].find('senID=')+6:])
		ws.append(fs[1])

	sen_dic2[sen_num]=' '.join(ws)



for sen_num in sen_dic2.keys():
	if sen_dic2[sen_num]!=sen_dic1[sen_num]:
		writer.write(str(sen_num))
		writer.write('\n')
		writer.write(sen_dic2[sen_num])
		writer.write('\n')
		writer.write(sen_dic1[sen_num])
		writer.write('\n')
		writer.write( '***********\n')



