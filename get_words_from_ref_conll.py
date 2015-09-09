# -*- coding: utf8
import os,sys,codecs

c1=codecs.open(os.path.abspath(sys.argv[1]),'r',encoding='utf-8').read().strip().replace('\r','').split('\n\n')
c2=codecs.open(os.path.abspath(sys.argv[2]),'r',encoding='utf-8').read().strip().split('\n\n')
writer=codecs.open(os.path.abspath(sys.argv[3]),'w',encoding='utf-8')

sen_dic1=dict()

for s in c1:
	ls=s.strip().split('\n')
	sen_num=0
	ws=list()
	lm=list()
	for l in ls:
		if not l.strip():
			continue
		fs=l.strip().split('\t')
		if sen_num==0:
			sen_num=int(fs[5][fs[5].find('senID=')+6:])
		ws.append(fs[1])
		lm.append(fs[2])

	sen_dic1[sen_num]=ws,lm

for s in c2:
	ls=s.strip().split('\n')
	sen_num=0
	ref=list()
	i=0

	ws=list()
	lms=list()
	for l in ls:
		fs=l.strip().split('\t')
		if sen_num==0:
			sen_num=int(fs[5][fs[5].find('senID=')+6:])
			ws=sen_dic1[sen_num][0]
			lms=sen_dic1[sen_num][1]

		fs[1]=ws[i]
		fs[2]=lms[i]
		i+=1

		writer.write('\t'.join(fs))
		writer.write('\n')
	writer.write('\n')
writer.close()
