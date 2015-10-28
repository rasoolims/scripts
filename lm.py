#! /usr/bin/python
# coding=utf8
 
from compiler.ast import Break

__author__="Mohammad Sadegh Rasooli <rasooli@cs.columbia.edu>"
__date__ ="Feb, 2013"

import sys
import os
import codecs
from collections import defaultdict
import operator
import math


sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

progDir=os.path.dirname(sys.argv[0])
if not progDir.endswith('/') and progDir!='':
    progDir+='/'
currdir=os.getcwd()

trainFile=os.path.abspath(sys.argv[1])
devFile=os.path.abspath(sys.argv[2])
outputLMFile=os.path.abspath(sys.argv[3])

fiveGramtable=defaultdict(float)
allFive=0.0
alphaFive=0.0
fourGramtable=defaultdict(float)
allFour=0.0
alphaFour=0.0
trigramtable=defaultdict(float)
allTri=0.0
alphaTri=0.0
bigramtable=defaultdict(float)
allBi=0.0
alphaBi=0.0
unigramtable=defaultdict(float)
allUni=0.0
alphaUni=0.0

lines=codecs.open(trainFile,'r',encoding='utf-8').read().split('\n')
count=0
for line in lines:
	count+=1
	if count%10000==0:
		print 'train',count
	sentence='<s> <s> <s> <s> '+line.strip()+' </s>'
	words=sentence.split(' ')
	for i in range(0,len(words)):
		allUni+=1
		unigramtable[words[i]]+=1.0
		if i<len(words)-1:
			allBi+=1
			bigramtable[words[i]+' '+words[i+1]]+=1.0
		if i<len(words)-2:
			allTri+=1
			trigramtable[words[i]+' '+words[i+1]+' '+words[i+2]]+=1.0
			if i<len(words)-3:
				allFour+=1
				fourGramtable[words[i]+' '+words[i+1]+' '+words[i+2]+' '+words[i+3]]+=1.0
				if i<len(words)-4:
					allFive+=1
					fiveGramtable[words[i]+' '+words[i+1]+' '+words[i+2]+' '+words[i+3]+' '+words[i+4]]+=1.0


print 'fivegram'
for five in fiveGramtable.keys():
	fourgram=five.split(' ')[0]+' '+five.split(' ')[1]+' '+five.split(' ')[2]+' '+five.split(' ')[3]
	fiveGramtable[five]/=fourGramtable[fourgram]
print 'fourgram'
for four in fourGramtable.keys():
	trigram=four.split(' ')[0]+' '+four.split(' ')[1]+' '+four.split(' ')[2]
	fourGramtable[four]/=trigramtable[trigram]
print 'trigram'
for tri in trigramtable.keys():
	bigram=tri.split(' ')[0]+' '+tri.split(' ')[1]
	trigramtable[tri]/=bigramtable[bigram]
	#print 'trigram\t'+tri+'\t'+str(trigramtable[tri])
print 'bigram'
for bi in bigramtable.keys():
	unigram=bi.split(' ')[0]
	bigramtable[bi]/=unigramtable[unigram]
	#print 'bigram\t'+bi+'\t'+str(bigramtable[bi])
print 'unigram'
for uni in unigramtable.keys():
	unigramtable[uni]/=allUni
	#print 'unigram\t'+uni+'\t'+str(unigramtable[uni])


devngramtable=defaultdict(float)
lines=codecs.open(devFile,'r',encoding='utf-8').read().split('\n')
count=0
for line in lines:
	count+=1
	if count%1000==0:
		print 'dev',count
	sentence='<s> <s> <s> <s>'+line.strip()+' </s>'
	words=sentence.split(' ')
	for i in range(0,len(words)):
		if i<len(words)-4:
			devngramtable[words[i]+' '+words[i+1]+' '+words[i+2]+' '+words[i+3]+' '+words[i+4]]+=1.0


l1=0.2
l2=0.2
l3=0.2
l4=0.2
l5=0.2
l6=0
smooth=0.000001
for i in range(1,20):
	c1=0.0
	c2=0.0
	c3=0.0
	c4=0.0
	c5=0.0
	c6=0.0
	print 'learning',i
	for five_gram in devngramtable.keys():
		spl = five_gram.split(' ')
		four=spl[1]+' '+spl[2]+' '+spl[3]+' '+spl[4]
		tri=spl[2]+' '+spl[3]+' '+spl[4]
		bi=spl[3]+' '+spl[4]
		uni=spl[4]

		five_prob=fiveGramtable[five_gram]
		four_prob=fourGramtable[four]
		triprob=trigramtable[tri]
		biprob=bigramtable[bi]
		uniprob=unigramtable[uni]
		
		cprime=devngramtable[five_gram]
		denom = l6 + l5*uniprob + l4*biprob + l3*triprob + l2*four_prob + l1*five_prob
		if denom!=0.0:
			c1+=(smooth/5+ cprime*l1*five_prob)/denom
			c2+=(smooth/5+ cprime*l2*four_prob)/denom
			c3+=(smooth/5+ cprime*l3*uniprob)/denom
			c4+=(smooth/5+ cprime*l4*biprob)/denom
			c5+=(smooth/5+ cprime*l5*uniprob)/denom
			c6+=cprime*l6/denom
	
	denom=c1+c2+c3+c4+c5+c6
	if denom!=0.0:
		l1=c1/denom
		l2=c2/denom
		l3=c3/denom
		l4=c4/denom
		l5=c5/denom
		l6=c6/denom
	print l1,l2,l3,l4,l5,l6


outopen=codecs.open(outputLMFile,'w',encoding='utf-8')
content=''
outopen.write('l1\t'+str(l1)+'\n')
outopen.write('l2\t'+str(l2)+'\n')
outopen.write('l3\t'+str(l3)+'\n')
outopen.write('l4\t'+str(l4)+'\n')
outopen.write('l5\t'+str(l5)+'\n')
outopen.write('l6\t'+str(l6)+'\n')
outopen.write('allUni\t'+str(allUni)+'\n')
outopen.write('allBi\t'+str(allBi)+'\n')
outopen.write('allTri\t'+str(allTri)+'\n')
outopen.write('allFour\t'+str(allFour)+'\n')
outopen.write('allFive\t'+str(allFive)+'\n')

print 'fivegram'
for gram in fiveGramtable.keys():
	outopen.write(  'fv\t'+gram+'\t'+str(fiveGramtable[gram])+'\n')
print 'fourgram'
for gram in fourGramtable.keys():
	outopen.write(  'fr\t'+gram+'\t'+str(trigramtable[gram])+'\n')
print 'trigram'
for tri in trigramtable.keys():
	outopen.write(  't\t'+tri+'\t'+str(trigramtable[tri])+'\n')
print 'bigrams'
for bi in bigramtable.keys():
	outopen.write(  'b\t'+bi+'\t'+str(bigramtable[bi])+'\n')
print 'unigrams'
for uni in unigramtable.keys():
	outopen.write(  'u\t'+uni+'\t'+str(unigramtable[uni])+'\n')


